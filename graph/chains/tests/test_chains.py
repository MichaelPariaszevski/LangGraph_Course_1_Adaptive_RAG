# def test_foo() -> None: # Run file using "pytest . -s -v"
#     assert 1==1

import os
import sys
from dotenv import load_dotenv, find_dotenv

print(os.getcwd())

sys.path.append(
    os.getcwd()
)  # Make sure to be in the final folder of the git repository in the terminal (where the code is being executed); make sure that os.getcwd is /home/mpariaszevski/LangChain_Courses/LangGraph_Advanced_RAG/LangGraph_Course_1_CRAG

load_dotenv(find_dotenv(), override=True)

from graph.chains.retrieval_grader import GradeDocuments, retrieval_grader_chain
from ingestion import retriever


def test_retrieval_grader_answer_yes() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)
    doc_text = docs[1].page_content  # Document with highest score

    response: GradeDocuments = retrieval_grader_chain.invoke(
        input={"document": doc_text, "question": question}
    )

    assert response.binary_score=="yes"

    # return response

    # "return response" is commented-out because this function (test_retireval_grader_answer_yes()) is meant to only serve as a test using pytest
    
example_response=test_retrieval_grader_answer_yes()

print(example_response)

# Run file using "pytest . -s -v" in the terminal