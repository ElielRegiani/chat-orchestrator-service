from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app


def test_health() -> None:
    c = TestClient(app)
    r = c.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@patch("integrations.insight_service_client.InsightServiceClient._post")
def test_webhook_consult_asset(mock_post) -> None:
    mock_post.return_value = {"answer": "PETR4 em alta."}
    c = TestClient(app)
    r = c.post(
        "/webhook",
        json={"from": "5511999999999", "message": "Como está PETR4?"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["to"] == "5511999999999"
    assert "PETR4" in data["message"] or "alta" in data["message"]
    mock_post.assert_called()


@patch("integrations.insight_service_client.InsightServiceClient._post")
def test_webhook_recommendation(mock_post) -> None:
    mock_post.return_value = {"answer": "Análise neutra."}
    c = TestClient(app)
    r = c.post(
        "/webhook",
        json={"from": "5511", "message": "Vale a pena comprar PETR4?"},
    )
    assert r.status_code == 200
    assert r.json()["message"] == "Análise neutra."
    assert mock_post.call_args is not None
    assert mock_post.call_args[0][0] == "/insight/ask"


@patch("integrations.insight_service_client.InsightServiceClient._post")
def test_webhook_summary(mock_post) -> None:
    mock_post.return_value = {"text": "Ibovespa subiu."}
    c = TestClient(app)
    r = c.post(
        "/webhook",
        json={"from": "5511", "message": "Resumo do mercado hoje"},
    )
    assert r.status_code == 200
    assert "Ibovespa" in r.json()["message"]


@patch("integrations.insight_service_client.InsightServiceClient._post")
def test_webhook_unknown(mock_post) -> None:
    mock_post.side_effect = AssertionError("should not call insight")
    c = TestClient(app)
    r = c.post(
        "/webhook",
        json={"from": "5511999999999", "message": "asdfgh random noise"},
    )
    assert r.status_code == 200
    assert "reformular" in r.json()["message"].lower()
