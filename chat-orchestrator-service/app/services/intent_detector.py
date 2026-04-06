import re

from app.schemas.message_schema import Intent

_TICKER_BR = re.compile(r"\b([A-Z]{4}\d)\b", re.IGNORECASE)

_SUMMARY_PATTERNS = (
    r"resumo\s+(do\s+)?mercado",
    r"mercado\s+hoje",
    r"como\s+foi\s+o\s+mercado",
    r"panorama\s+do\s+mercado",
    r"fechamento\s+do\s+mercado",
)

_RECOMMENDATION_PATTERNS = (
    r"vale\s+a\s+pena",
    r"devo\s+comprar",
    r"devo\s+investir",
    r"é\s+um\s+bom\s+momento",
    r"recomend",
    r"compensa\s+comprar",
    r"vale\s+comprar",
)

_CONSULT_PATTERNS = (
    r"como\s+está",
    r"como\s+esta",
    r"pre[cç]o\s+(da|do|de)",
    r"cota[cç][aã]o",
    r"como\s+anda",
    r"status\s+(da|do|de)",
)


def _match_any(patterns: tuple[str, ...], text: str) -> bool:
    lowered = text.lower()
    for p in patterns:
        if re.search(p, lowered, re.IGNORECASE):
            return True
    return False


def extract_tickers(text: str) -> list[str]:
    found = _TICKER_BR.findall(text.upper())
    # dedupe preserving order
    seen: set[str] = set()
    out: list[str] = []
    for t in found:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def detect_intent(message: str) -> Intent:
    text = message.strip()
    if not text:
        return Intent.UNKNOWN

    if _match_any(_SUMMARY_PATTERNS, text):
        return Intent.MARKET_SUMMARY

    if _match_any(_RECOMMENDATION_PATTERNS, text):
        return Intent.ASK_RECOMMENDATION

    if _match_any(_CONSULT_PATTERNS, text) or extract_tickers(text):
        return Intent.CONSULT_ASSET

    return Intent.UNKNOWN
