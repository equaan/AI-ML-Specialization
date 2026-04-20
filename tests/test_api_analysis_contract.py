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


def test_persisted_report_is_listed_and_retrievable() -> None:
    analyze_response = client.post("/api/analyze", data={"symptoms": "chest pain and fatigue"})
    assert analyze_response.status_code == 200
    session_id = analyze_response.json()["session_id"]

    list_response = client.get("/api/reports", params={"limit": 10})
    assert list_response.status_code == 200
    listed_ids = [item["session_id"] for item in list_response.json().get("reports", [])]
    assert session_id in listed_ids

    get_response = client.get(f"/api/reports/{session_id}")
    assert get_response.status_code == 200
    payload = get_response.json()
    assert payload["session_id"] == session_id
    assert "report" in payload


def test_analyze_pe_like_case_includes_pe_or_pleurisy_and_dynamic_steps() -> None:
    response = client.post(
        "/api/analyze",
        data={
            "symptoms": (
                "sudden shortness of breath, pleuritic chest pain, tachycardia, "
                "and elevated d-dimer with oxygen saturation drop"
            )
        },
    )
    assert response.status_code == 200
    report = response.json()["report"]

    diagnoses = [item["condition"].lower() for item in report.get("differential_diagnosis", [])]
    assert any("pulmonary embolism" in name or "pleurisy" in name for name in diagnoses)

    steps_blob = " ".join(report.get("recommended_next_steps", [])).lower()
    assert "ct pulmonary angiography" in steps_blob or "d-dimer" in steps_blob
