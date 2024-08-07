from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class GradeAnswer(BaseModel):
    binary_score: bool = Field(
        description="Answer addresses the question, 'True' or 'False'."
    )


structured_llm_grader = llm.with_structured_output(GradeAnswer)

system = """You are a grader accessing whether an answer addresses or resolves the question asked by the user. \n 
Give a binary score 'True' or 'False'. 'True' means that the answer addresses or resolves the question asked by the user."""

answer_grader_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
    ]
)

answer_grader_chain: RunnableSequence = answer_grader_prompt | structured_llm_grader
