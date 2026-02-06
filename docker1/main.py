from fastapi import FastAPI

app = FastAPI()

#  Задание 1
# @app.get("/")
# async def hello():
#     return "Hello from Docker!"




#  Задание 2
@app.get("/")
async def hello():
    return { "message": "Hello, FastAPI!" }


@app.get("/health")
async def health():
    return { "status": "ok" }


@app.get("/items/{item_id}")
async def items(item_id: int):
    return { "item": item_id }

