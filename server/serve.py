from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
import os

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

import phoenix as px
import pandas as pd
import numpy as np

from phoenix.trace.langchain import OpenInferenceTracer, LangChainInstrumentor

index_label = 'index-1'

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY']) # set openai_api_key = 'your_openai_api_key'

pinecone.init(
            api_key= os.environ['PINECONE_API_KEY'], # set api_key = 'yourapikey'
            environment= 'gcp-starter'
)
index_name = pinecone.Index(index_label)

vectorstore = Pinecone.from_existing_index(index_label, embeddings)

retriever = vectorstore.as_retriever()



qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(model_name='gpt-3.5-turbo',temperature=0), retriever, return_source_documents=True)

# qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), retriever, return_source_documents=True)

app = FastAPI()


# If no exporter is specified, the tracer will export to the locally running Phoenix server
tracer = OpenInferenceTracer()
LangChainInstrumentor(tracer).instrument()


# Create a Pydantic model to define the expected data structure in the request body
class Item(BaseModel):
    query: str

# Define a POST route to create a new item
@app.post("/items/")
async def create_item(item: Item):
    # In this example, the data sent in the request body is automatically parsed
    # and validated based on the Item model.
    # You can process and store the received data as needed.


    chat_history = []  # Initialize chat history for conversation
    result = qa({"question": item.query, "chat_history": chat_history}, callbacks=[tracer])
    answer = result['answer']
    source_documents = result['source_documents'][0] if result['source_documents'] else []


    return {"answer": result['answer'], "source_documents": result['source_documents'][0]}


