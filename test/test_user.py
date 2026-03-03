from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "World War loading"}

def test_create_user():
    res = client.post("/users/", json={"email": "heloahdu@gmail.com", "password": "password123"})
    print(res.json())
    assert res.status_code ==201