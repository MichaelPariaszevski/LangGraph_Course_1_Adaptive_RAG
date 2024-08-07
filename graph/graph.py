from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

# import os
# import sys

# print(sys.path)
# sys.path.append("/home/mpariaszevski/LangChain_Courses/LangGraph_Advanced_RAG/LangGraph_Course_1_CRAG/graph/state")

from langgraph.graph import END, StateGraph
from graph.chains.answer_grader import answer_grader_chain
from graph.chains.hallucination_grader import hallucination_grader_chain
from graph.constants import RETRIEVE, GRADE_DOCUMENTS, WEB_SEARCH, GENERATE
from graph.nodes import retrieve, grade_documents, web_search, generate
from graph.state import GraphState


def decide_to_generate(state):
    print("---Assess Graded Documents---")

    if state[
        "web_search"
    ]:  # found a document that is not relevant to the user's question/query
        print(
            f"---Decision: Not All Documents Are Relevant to Question: {state['question']}"
        )
        return WEB_SEARCH
    else:
        print("---Decision: Generate---")
        return GENERATE


def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
    print("---Check Hallucinations---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score = hallucination_grader_chain.invoke(
        {"documents": documents, "generation": generation}
    )

    if hallucination_grade := score.binary_score:
        print("---Decision: Generation is grounded in Documents---")
        print("---Grade Generation vs Question---")
        score_answer = answer_grader_chain.invoke(
            {"question": question, "generation": generation}
        )
        if answer_grade := score_answer.binary_score:
            print("---Decision: Generation Addresses Question---")
            return "useful"
        else:  # if answer is grounded in the documents but does not answer the question
            print(f"---Decision: Generation Does Not Address The Question: {question}")
            return "not useful"
    else:  # if answer is not grounded in the documents
        print("---Decision: Generation Is Not Grounded In Documents---")
        return "not grounded"


workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(WEB_SEARCH, web_search)
workflow.add_node(GENERATE, generate)

workflow.set_entry_point(RETRIEVE)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    path_map={WEB_SEARCH: WEB_SEARCH, GENERATE: GENERATE},
)  # path_map shows options for the conditional_edge

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    path_map={"not grounded": GENERATE, "useful": END, "not useful": WEB_SEARCH},
)

workflow.add_edge(WEB_SEARCH, GENERATE)
workflow.add_edge(GENERATE, END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="self_RAG_original_graph.png")
