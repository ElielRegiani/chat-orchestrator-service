import pytest

from app.schemas.message_schema import Intent
from app.services.intent_detector import detect_intent, extract_tickers


@pytest.mark.parametrize(
    ("msg", "expected"),
    [
        ("Como está PETR4?", Intent.CONSULT_ASSET),
        ("Preço da VALE3 hoje", Intent.CONSULT_ASSET),
        ("PETR4", Intent.CONSULT_ASSET),
        ("Vale a pena comprar VALE3?", Intent.ASK_RECOMMENDATION),
        ("É um bom momento para investir em BTC?", Intent.ASK_RECOMMENDATION),
        ("Resumo do mercado hoje", Intent.MARKET_SUMMARY),
        ("Como foi o mercado hoje?", Intent.MARKET_SUMMARY),
        ("xyz random", Intent.UNKNOWN),
    ],
)
def test_detect_intent(msg: str, expected: Intent) -> None:
    assert detect_intent(msg) == expected


def test_extract_tickers() -> None:
    assert extract_tickers("PETR4 e VALE3") == ["PETR4", "VALE3"]
