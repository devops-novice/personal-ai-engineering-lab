import json

from fastapi.testclient import TestClient

import audit
import main
from schemas import TriageResponse


client = TestClient(main.app)


def fake_triage_response(priority: str = "medium") -> TriageResponse:
    return TriageResponse(
        category="incident" if priority in {"high", "critical"} else "other",
        priority=priority,
        summary="Synthetic triage summary.",
        missing_information=["affected users", "start time"],
        human_review_required=priority in {"high", "critical"},
        confidence=0.82,
    )


def test_triage_deployment_or_performance_incident(monkeypatch, tmp_path):
    audit_path = tmp_path / "audit.log"
    monkeypatch.setattr(main, "triage_request", lambda _: fake_triage_response("high"))
    monkeypatch.setattr(
        main,
        "write_audit_event",
        lambda **kwargs: audit.write_audit_event(
            **kwargs,
            audit_log_path=audit_path,
        ),
    )

    response = client.post(
        "/triage",
        json={
            "request": "Deployment failed twice after the latest change and login is slow."
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["priority"] == "high"
    assert body["human_review_required"] is True
    assert 0 <= body["confidence"] <= 1

    audit_text = audit_path.read_text(encoding="utf-8")
    audit_event = json.loads(audit_text.strip())
    assert "Deployment failed" not in audit_text
    assert audit_event["input_length"] > 0
    assert audit_event["priority"] == "high"


def test_triage_vague_input(monkeypatch):
    monkeypatch.setattr(main, "triage_request", lambda _: fake_triage_response("medium"))
    monkeypatch.setattr(main, "write_audit_event", lambda **_: None)

    response = client.post("/triage", json={"request": "Something is broken."})

    assert response.status_code == 200
    assert response.json()["missing_information"]


def test_triage_low_priority_improvement(monkeypatch):
    monkeypatch.setattr(main, "triage_request", lambda _: fake_triage_response("low"))
    monkeypatch.setattr(main, "write_audit_event", lambda **_: None)

    response = client.post(
        "/triage",
        json={"request": "Please improve the wording in the internal sample README."},
    )

    assert response.status_code == 200
    assert response.json()["priority"] == "low"
    assert response.json()["human_review_required"] is False


def test_empty_input_validation():
    response = client.post("/triage", json={"request": ""})

    assert response.status_code == 422
