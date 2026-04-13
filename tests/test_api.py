from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root_endpoint_returns_message() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "MediAgent API is running"
