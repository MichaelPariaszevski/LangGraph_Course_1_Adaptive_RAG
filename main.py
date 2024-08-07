from dotenv import load_dotenv, find_dotenv 

load_dotenv(find_dotenv(), override=True) 

from graph.graph import app

if __name__ == "__main__": 
    print("Hello Corrective RAG")
    output=app.invoke(input={"question": "What is agent memory?"}) 
    print(output)
    print(output.keys())