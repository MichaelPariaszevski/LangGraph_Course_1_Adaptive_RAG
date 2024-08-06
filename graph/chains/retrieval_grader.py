# Returns whether a document is relevant to the search query or not
# import sys
# import os

# sys.path.append(os.getcwd())

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

# from dotenv import load_dotenv, find_dotenv

# load_dotenv(find_dotenv(), override=True)

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)


class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"  # LLM uses this description to decide whether the document is relevant or not
    )


# To use ".with_structured_output()" our LLM must support function calling
structured_llm_grader = llm.with_structured_output(
    GradeDocuments
)  # Uses function calling and, for every LLM call that we make, we are going to return a Pydantic object (Pydantic object in the schema that we want)

system = """Your are a grader assessing relevance of a retrieved document to a user question. \n 
If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. \n 
Give a binary score 'yes' or 'no' to indicate whether the document is relevant to the question."""

grade_prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)

retrieval_grader_chain = grade_prompt | structured_llm_grader
