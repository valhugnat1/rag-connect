from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import time

from pydantic import BaseModel

import uvicorn
app = FastAPI()

from llama_index.llms.openai_like import OpenAILike
import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)


PERSIST_DIR = "./storage"
llm = OpenAILike(api_base="http://f916afca-1d75-4ee5-992c-9f94e9ab1b57.pub.instances.scw.cloud:8000/v1", 
                 model="TheBloke/Mistral-7B-Instruct-v0.2-AWQ", 
                 max_tokens= 400,
                 temperature=0,
                 api_key="hugo-secret-token"
                )

storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
index = load_index_from_storage(storage_context)

# Either way we can now query the index
query_engine = index.as_query_engine()

query_engine_vllm = index.as_query_engine(llm=llm)

def vllm_streamer(question):

    # stream_response = llm.stream_complete("what is a black hole")

    stream_response = query_engine_vllm.query("What is the author name?").response_gen

    for line in stream_response:
        yield f"{line}"

def fake_streamer():

    global llm

    response = llm.complete("<s>[INST] Hello, explain 10 idea to be a good product manager [/INST]")
    print(str(response))
    for i in range(10):
        yield f"some fake stream : " + str(i)
        time.sleep(1)


class Question(BaseModel):
    question: str

class Question(BaseModel):
    question: str



@app.post("/")
async def main(question_body: Question):
    question = question_body.question
    return StreamingResponse(vllm_streamer(question), headers={ "Content-Type": "text/event-stream" })

