# def test_foo() -> None: # Run file using "pytest . -s -v"
#     assert 1==1

# import os
# import sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

# print(os.getcwd())

# sys.path.append(
#     os.getcwd()
# )  # Make sure to be in the final folder of the git repository in the terminal (where the code is being executed); make sure that os.getcwd is /home/mpariaszevski/LangChain_Courses/LangGraph_Advanced_RAG/LangGraph_Course_1_CRAG

from graph.chains.retrieval_grader import GradeDocuments, retrieval_grader_chain
from graph.chains.generation import generation_chain
from ingestion import retriever

from graph.chains.hallucination_grader import GradeHallucinations, hallucination_grader_chain

from pprint import pprint # pprint or pretty print


def test_retrieval_grader_answer_yes() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)
    doc_text = docs[0].page_content  # Document with highest score

    response: GradeDocuments = retrieval_grader_chain.invoke(
        input={"document": doc_text, "question": question}
    )

    assert response.binary_score == "yes"

    # return response

    # "return response" is commented-out because this function (test_retireval_grader_answer_yes()) is meant to only serve as a test using pytest


def test_retrieval_grader_answer_no() -> None:
    question = "How to make pizza"
    docs = retriever.invoke(question)
    doc_text = docs[0].page_content  # Document with highest score

    response: GradeDocuments = retrieval_grader_chain.invoke(
        input={"document": doc_text, "question": question}
    )

    assert response.binary_score == "no"

# Run file using "pytest . -s -v" in the terminal

def test_generation_chain() -> None: 
    question ="agent memory" 
    docs=retriever.invoke(question) 
    generation=generation_chain.invoke({"context": docs, "question": question})
    pprint(generation)
    
# test_generation_chain()

def test_hallucination_grader_answer_yes() -> None: 
    question="agent memory" 
    docs=retriever.invoke(question) 
    generation=generation_chain.invoke({"context": docs, "question": question}) 
    response: GradeHallucinations=hallucination_grader_chain.invoke({"documents": docs, "generation": generation}) 
    
    assert response.binary_score==True

def test_hallucination_grader_answer_no() -> None: 
    question="agent memory" 
    docs=retriever.invoke(question) 
    # generation=generation_chain.invoke({"context": docs, "question": question}) 
    response: GradeHallucinations=hallucination_grader_chain.invoke({"documents": docs, "generation": "In order to make pizza we need to first start with the dough"}) 
    
    assert response.binary_score==False

# Run file using "pytest . -s -v" in the terminal
