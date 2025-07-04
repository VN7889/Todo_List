from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Response, Depends
from fastapi.encoders import jsonable_encoder 
from core.database.models import Todo, TodoCU, create_db_and_tables, get_session, create_todo_item, remove_todo_item, read_todo_items, read_item, update_todo_item
from sqlmodel import SQLModel, Session
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager # type: ignore
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    
app = FastAPI(lifespan=lifespan)

origins = [
        "http://127.0.0.1:5500/frontend/",
        "http://localhost:5500/frontend/",
        "*"
]
app.add_middleware(
  CORSMiddleware,
  allow_origins = origins,
  allow_credentials=True,
  allow_methods = ["*"],
  allow_headers = ["*"]
)

class Message(SQLModel):
    message: str

@app.get("/items")
def read_items(session: Session = Depends(get_session))->list[Todo]:
    return read_todo_items(session) # type: ignore

@app.get("/items/{id}", responses={404: {"model": Message}})
def get_item(id: int, session: Session = Depends(get_session)):
    item= read_item(id, session)
    if item is not None:
        return item
    raise HTTPException(status_code=404, detail=f"Item with id '{id}' not found!")


@app.post("/create_items/")
def create_item(item: TodoCU, session: Session = Depends(get_session)):
    add_item= create_todo_item(item, session)
    return add_item


@app.put("/update_items/{id}", responses={404: {"model": Message}})
async def update_items(id: int, item: TodoCU, session: Session = Depends(get_session)):
    update_item= update_todo_item(id, item, session)
    if update_item is not None:
        return update_item
    raise HTTPException(404, f"Item with id '{id}' not found!")


@app.delete("/remove_items/{id}", responses={404: {"model": Message}})
def remove_item(id: int, session: Session = Depends(get_session)):
    delete_item= remove_todo_item(id, session)
    if delete_item is not None:
        return delete_item
    raise HTTPException(404, f"Item with id '{id}' not found!")
