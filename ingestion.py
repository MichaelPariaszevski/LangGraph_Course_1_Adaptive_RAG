from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

docs = [
    WebBaseLoader(url).load() for url in urls
]  # Each item of this list is a LangChain Document object

docs_list = [
    item for sublist in docs for item in sublist
]  # The outer loop ("for sublist in docs") iterates over each sublist in the docs list.
# The inner loop ("for item in sublist") iterates over each item in the current sublist.
# The expression ("item") represents each individual item in the nested list.
# By placing it at the beginning of the expression, we are telling Python to include that item in the new list.

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)

docs_split = text_splitter.split_documents(docs_list)

# vector_store = Chroma.from_documents(
#     documents=docs_split,
#     collection_name="CRAG_Chroma",
#     embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
#     persist_directory="./.chroma",
# )

retriever = Chroma(
    collection_name="CRAG_Chroma",
    persist_directory="./.chroma",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
).as_retriever

if __name__ == "__main__":
    # print(docs)
    pass
