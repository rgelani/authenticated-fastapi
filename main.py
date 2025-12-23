from fastapi import FastAPI
from pydentic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    email: str | None = none
    password: str
    created_at: Optional[datetime] = None


@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "item_name": "Test"}