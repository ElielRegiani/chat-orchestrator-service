import logging

import httpx

from app.schemas.message_schema import (
    InsightAskRequest,
    InsightExplainRequest,
    InsightResponse,
    Intent,
)
from app.services.intent_detector import extract_tickers
from integrations.insight_service_client import InsightServiceClient

logger = logging.getLogger(__name__)

_FALLBACK = "Não entendi sua pergunta. Pode reformular?"
_SERVICE_UNAVAILABLE = (
    "Não consegui consultar o serviço de análise no momento. Tente novamente em instantes."
)


class Orchestrator:
    def __init__(self, insight: InsightServiceClient) -> None:
        self._insight = insight

    def run(self, intent: Intent, user_text: str) -> InsightResponse:
        text = user_text.strip()
        tickers = extract_tickers(text)
        primary_ticker = tickers[0] if tickers else None

        try:
            if intent == Intent.MARKET_SUMMARY:
                return self._insight.summary()
            if intent == Intent.ASK_RECOMMENDATION:
                return self._insight.ask(
                    InsightAskRequest(question=text, ticker=primary_ticker)
                )
            if intent == Intent.CONSULT_ASSET:
                return self._insight.explain(
                    InsightExplainRequest(ticker=primary_ticker, question=text)
                )
        except httpx.HTTPError:
            logger.exception("orchestrator_insight_call_failed")
            return InsightResponse(text=_SERVICE_UNAVAILABLE)

        return InsightResponse(text=_FALLBACK)
