from fastapi import FastAPI

app = FastAPI(title="Task Management API")


@app.get("/")
async def root():
    """
    returns the main message
    """
    return {"Message", "Welcome to the task management app"}


@app.get("/hello/{name}")
async def hello(name: str):
    """
    test for api params
    """
    return {"Message", f"Hello {name}"}
