from typing import Literal # Literal indicates that a variable can only take one of a predefined set of values

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field # For a structured LLM output
from langchain_openai import ChatOpenAI

class RouteQuery(BaseModel): 
    """Route a user query to the most relevant datasource""" 
    datasource: Literal["vectorstore", "websearch"]=Field(..., description="Given a user question choose to route it to a web search or to a vectorstore.") 
    
llm=ChatOpenAI(model="gpt-4o-mini", temperature=0) 

structured_llm_router=llm.with_structured_output(RouteQuery)

system="""You are an expert at routing a user question to a vectorstore or a web search. 
The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks. 
Use the vectorstore for questions on these topcs. For all else, use web-search."""

router_prompt=ChatPromptTemplate.from_messages(messages=[("system", system), ("human", "{question}")]) 

question_router_chain=router_prompt | structured_llm_router   