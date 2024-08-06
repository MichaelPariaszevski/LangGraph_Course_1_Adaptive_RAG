from typing import Any, Dict 

# import os 
# import sys 

# sys.path.append("/home/mpariaszevski/LangChain_Courses/LangGraph_Advanced_RAG/LangGraph_Course_1_CRAG")
# sys.path.append("/home/mpariaszevski/LangChain_Courses/LangGraph_Advanced_RAG/LangGraph_Course_1_CRAG/graph")
# sys.path.append("/home/mpariaszevski/LangChain_Courses/LangGraph_Advanced_RAG/LangGraph_Course_1_CRAG/graph/chains")


# for i in sys.path: 
#     print("-"*50)
#     print("\n")
#     print(i)

from graph.chains.generation import generation_chain 
from graph.state import GraphState

def generate(state: GraphState) -> Dict[str, Any]: 
    print("---Generate---") 
    question=state["question"] 
    documents=state["documents"] 
    
    generation=generation_chain.invoke({"question": question, "context": documents}) 
    return {"documents": documents, "question": question, "generation": generation} # {"generation": generation} is the answer that the llm responded