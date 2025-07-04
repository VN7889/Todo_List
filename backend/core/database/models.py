from typing import Generator
from sqlmodel import Field, SQLModel, Session, create_engine, select


class Todo(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class TodoCU(SQLModel):
    # id: int | None = None
    name: str

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"


engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# Print all the data from database.
def read_todo_items(session: Session):
    statement = select(Todo)
    results = session.exec(statement).all()
    return results

# Print item by id.
def read_item(id: int, session: Session):
    db_item = session.get(Todo, id)
    if not db_item:
        return 
    return {"id": db_item.id, "name": db_item.name}

# create data in the database.
def create_todo_item(item: TodoCU, session: Session):
    todo_item = Todo.model_validate(item)
    session.add(todo_item)
    session.commit()
    session.refresh(todo_item)
    return {"id": todo_item.id, "name": todo_item.name, "msg": "Item added successfully."}

# Update the data in the database.
def update_todo_item(id: int, item: TodoCU, session: Session):
    db_item = session.get(Todo, id)
    if not db_item:
        return
    db_item.name = item.name
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return {"id": db_item.id, "name": db_item.name, "msg": "Item updated successfully"}

# Delete data from the database.
def remove_todo_item(id: int, session: Session):
    db_item = session.get(Todo, id)
    if not db_item:
        return 
    session.delete(db_item)
    session.commit()
    return {"id" : db_item.id, "name": db_item.name, "msg": "Item removed successfully."}

