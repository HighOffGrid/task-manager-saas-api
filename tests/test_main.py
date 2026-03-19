from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root(client):
    response = client.get("/")
    body = response.json()

    assert response.status_code == 200
    assert "message" in body
    assert body["message"] == "API running"