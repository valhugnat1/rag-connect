from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import time

import uvicorn
app = FastAPI()

from llama_index.llms.openai_like import OpenAILike
llm = OpenAILike(api_base="http://f916afca-1d75-4ee5-992c-9f94e9ab1b57.pub.instances.scw.cloud:8000/v1", 
                 model="TheBloke/Mistral-7B-Instruct-v0.2-AWQ", 
                 max_tokens= 400,
                 temperature=0,
                 api_key="hugo-secret-token"
                )

def vllm_streamer():

    stream_response = llm.stream_complete("what is a black hole")
    print (stream_response)

    for line in stream_response:
        yield f"{line}"

def fake_streamer():

    global llm

    response = llm.complete("<s>[INST] Hello, explain 10 idea to be a good product manager [/INST]")
    print(str(response))
    for i in range(10):
        yield f"some fake stream : " + str(i)
        time.sleep(1)



@app.get("/")
async def main():
    return StreamingResponse(vllm_streamer(), headers={ "Content-Type": "text/event-stream" })

