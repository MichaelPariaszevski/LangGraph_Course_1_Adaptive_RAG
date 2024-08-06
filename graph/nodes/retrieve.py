from typing import Any, Dict 

# import os 
# import sys 

# sys.path.append("/home/mpariaszevski/LangChain_Courses/LangGraph_Advanced_RAG/LangGraph_Course_1_CRAG/graph")
# sys.path.append("/home/mpariaszevski/LangChain_Courses/LangGraph_Advanced_RAG/LangGraph_Course_1_CRAG/graph/chains")
# sys.path.append("/home/mpariaszevski/LangChain_Courses/LangGraph_Advanced_RAG/LangGraph_Course_1_CRAG")


# for i in sys.path: 
#     print("-"*50)
#     print("\n")
#     print(i)

from graph.state import GraphState
from ingestion import retriever # Chroma vector store as retriever

def retrieve(state: GraphState) -> Dict[str, Any]: 
    print("---Retrieve---") 
    question=state["question"]
    
    documents=retriever.invoke(question) 
    
    return {"documents": documents, "question": question} # Updates the state/GraphState object