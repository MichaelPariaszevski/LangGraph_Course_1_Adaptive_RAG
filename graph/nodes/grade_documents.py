from typing import Any, Dict

from graph.chains.retrieval_grader import retrieval_grader_chain
from graph.state import GraphState


def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question.
    If any document is not relevant, we will set a flag to run a web search

    Args:
        state (GraphState): The current graph state

    Returns:
        Dict[str, Any]: Filtered out irrelevant documents and updated web_search state
    """

    print("---Checking Document Relevance Compared to Question---")
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []  # Append to list every relevant document
    web_search = False
    for d in documents:
        score = retrieval_grader_chain.invoke(
            input={"question": question, "document": d.page_content}
        )
        grade=score.binary_score 
        if grade.lower()=="yes": 
            print("---Grade: Document Relevant---") 
            filtered_docs.append(d) 
        elif grade.lower()=="no": 
            print("---Grade: Document Not Relevant---") 
            web_search=True # Even if only one of the documents is scored as not relevant, set web_search to True and leave it there regardless of the other documents
            continue
    return {"documents": filtered_docs, "question": question, "web_search": web_search}
        
