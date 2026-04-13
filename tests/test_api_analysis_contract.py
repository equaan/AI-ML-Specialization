from io import BytesIO

from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_analyze_requires_at_least_one_input() -> None:
    response = client.post("/api/analyze", data={"symptoms": ""})
    assert response.status_code == 400


def test_analyze_with_symptoms_returns_session_id_and_report() -> None:
    response = client.post("/api/analyze", data={"symptoms": "fever and cough"})
    assert response.status_code == 200
    payload = response.json()
    assert "session_id" in payload
    assert "report" in payload
    assert "disclaimer" in payload["report"]
