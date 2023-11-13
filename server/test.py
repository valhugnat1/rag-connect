from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a simple route
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}
