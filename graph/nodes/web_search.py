from typing import Any, Dict

import sys
import os 

sys.path.append(os.getcwd())

from langchain.schema import Document
from langchain_community.tools.tavily_search import TavilySearchResults

from graph.state import GraphState

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

web_search_tool = TavilySearchResults(max_results=3)


def web_search(state: GraphState) -> Dict[str, Any]:
    print("---Web Search---")
    question = state["question"]
    documents = state["documents"]

    tavily_results = web_search_tool.invoke({"query": question})
    joined_tavily_results = "\n".join(
        [tavily_result["content"] for tavily_result in tavily_results]
    )

    web_results = Document(page_content=joined_tavily_results) 
    
    if documents is not None: 
        documents.append(web_results) 
    else: 
        documents=[web_results] 
    return {"question": question, "documents": documents}

if __name__ =="__main__": 
    result=web_search(state={"question": "agent_memory", "documents": None})  
    print(result)
    
