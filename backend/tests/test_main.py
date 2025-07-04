import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, StaticPool, create_engine, Session
from main import app
from core.database.models import Todo, get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")  
def client_fixture(session: Session):  
    def get_session_override():  
        return session

    app.dependency_overrides[get_session] = get_session_override  

    client = TestClient(app)  
    yield client  
    app.dependency_overrides.clear()


def test_create_item(client: TestClient):
    response = client.post("/create_items/",json={"name": "Test Item"})
    item_id = response.json().get(id,1)
    assert response.status_code == 200
    assert response.json() == {"id": item_id, "name": "Test Item", "msg": "Item added successfully."}

def test_read_items(client: TestClient):
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_item_existing(client: TestClient):
    post_response = client.post("/create_items/",json={"name": "Read Item"})
    item_id = post_response.json().get("id", 1)
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Read Item"}

def test_read_item_non_existing(client: TestClient):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item with id '999' not found!"}

def test_read_item_invalid_id(client: TestClient):
    response = client.get("/items/abc")
    assert response.status_code == 422
    assert "Input should be a valid integer" in response.json()["detail"][0]["msg"]

def test_update_item(client: TestClient):
    post_response = client.post("/create_items/",json={"name": "Old Item"})
    item_id = post_response.json().get("id", 1)
    response = client.put(f"/update_items/{item_id}",json={"name": "Updated Item"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Updated Item", "msg": "Item updated successfully"}

def test_update_item_non_existing(client: TestClient):
    response = client.put(f"/update_items/999",json={"name": "Updated Item"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item with id '999' not found!"}

def test_remove_item(client: TestClient):
    post_response = client.post("/create_items/",json={"name": "Delete Me"})
    item_id = post_response.json().get("id", 1)
    response = client.delete(f"/remove_items/{item_id}")
    assert response.status_code == 200
    assert response.json() == {"id" : 1, "name": "Delete Me", "msg": "Item removed successfully."}

def test_remove_item_non_existing(client: TestClient):
    response = client.delete("/remove_items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item with id '999' not found!"}