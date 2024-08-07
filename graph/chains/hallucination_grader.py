from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in the generated answer.

    Args:
        BaseModel (_type_): BaseModel from Pydantic enforces a defined output structure
    """

    binary_score: bool = Field(
        description="If the answerif gorunded in the facts provided from the docuemnts, 'True' or 'false'."
    )  # Because the type hint for binary_score is boolean, the langchain output parser will output the LLM's response as a boolean


structured_llm_grader = llm.with_structured_output(schema=GradeHallucinations)

system = """You are a grader assessing whether an LLM generated answer is grounded in or supported by a set of documents. 
Give a binary score of 'True' or 'False'. 'True' means that the ansewr is grounded in or supported by the documents."""

hallucination_prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", system),
        (
            "human",
            "Set of facts: \n\n {documents} \n\n LLM generated answer: {generation}",
        ),
    ]
)

hallucination_grader_chain: RunnableSequence = (
    hallucination_prompt | structured_llm_grader
)
