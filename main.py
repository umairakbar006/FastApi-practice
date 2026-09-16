from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Welcome to my api"}

@app.post("/items")
def read_root():
    return {"Items": "These are my items"}