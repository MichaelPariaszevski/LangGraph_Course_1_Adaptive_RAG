from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

prompt = hub.pull("rlm/rag-prompt")

# rlm/rag-prompt:

# You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you
# don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
# Question: {question}
# Context: {context}
# Answer:

# To invoke the chain, {"question": example_question, "context": example_context} is needed

generation_chain = prompt | llm | StrOutputParser()
