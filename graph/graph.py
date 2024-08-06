from dotenv import load_dotenv, find_dotenv 

load_dotenv(find_dotenv(), override=True) 

# import os 
# import sys 

# print(sys.path)
# sys.path.append("/home/mpariaszevski/LangChain_Courses/LangGraph_Advanced_RAG/LangGraph_Course_1_CRAG/graph/state")

from langgraph.graph import END, StateGraph 
from graph.constants import RETRIEVE, GRADE_DOCUMENTS, WEB_SEARCH, GENERATE 
from graph.nodes import retrieve, grade_documents, web_search, generate 
from graph.state import GraphState

def decide_to_generate(state): 
    print("---Assess Graded Documents---") 
    
    if state["web_search"]: # found a document that is not relevant to the user's question/query 
        print(f"---Decision: Not All Documents Are Relevant to Question: {state['question']}")
        return WEB_SEARCH
    else: 
        print("---Decision: Generate---") 
        return GENERATE
    
workflow=StateGraph(GraphState) 

workflow.add_node(RETRIEVE, retrieve) 
workflow.add_node(GRADE_DOCUMENTS, grade_documents) 
workflow.add_node(WEB_SEARCH, web_search) 
workflow.add_node(GENERATE, generate) 

workflow.set_entry_point(RETRIEVE) 
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS) 
workflow.add_conditional_edges(GRADE_DOCUMENTS, decide_to_generate, path_map={WEB_SEARCH: WEB_SEARCH, GENERATE: GENERATE}) # path_map shows options for the conditional_edge
workflow.add_edge(WEB_SEARCH, GENERATE) 
workflow.add_edge(GENERATE, END) 

app=workflow.compile() 

app.get_graph().draw_mermaid_png(output_file_path="graph.png")