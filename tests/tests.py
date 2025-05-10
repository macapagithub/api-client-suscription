from fastapi.testclient import TestClient
from fastapi import status

def test_client(client):
    """Test the FastAPI client."""
    assert type(client) == TestClient

def test_create_client(client):
    """Test creating a client."""
    response = client.post("/clients/", json={"name": "Mauricio", 
                                              "age": 40,
                                              "email": "mauricio@test.com"})

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Mauricio"
    assert data["age"] == 40
    assert data["email"] == "mauricio@test.com"
