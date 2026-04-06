import logging
from typing import Any

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from app.config.settings import Settings
from app.schemas.message_schema import (
    InsightAskRequest,
    InsightExplainRequest,
    InsightResponse,
    InsightSummaryRequest,
)

logger = logging.getLogger(__name__)


def _should_retry(exc: BaseException) -> bool:
    if isinstance(exc, (httpx.TimeoutException, httpx.NetworkError)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        s = exc.response.status_code
        return s >= 500 or s == 429
    return False


class InsightServiceClient:
    def __init__(self, settings: Settings) -> None:
        self._base = settings.insight_service_url.rstrip("/")
        self._timeout = httpx.Timeout(settings.insight_timeout_seconds)
        self._attempts = settings.insight_max_retries

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=8),
        retry=retry_if_exception(_should_retry),
    )
    def _post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        url = f"{self._base}{path}"
        with httpx.Client(timeout=self._timeout) as client:
            r = client.post(url, json=body)
            r.raise_for_status()
            return r.json() if r.content else {}

    def explain(self, req: InsightExplainRequest) -> InsightResponse:
        body = req.model_dump(exclude_none=True)
        try:
            data = self._post("/insight/explain", body)
        except httpx.HTTPError as e:
            logger.exception("insight_explain_failed", extra={"error": str(e)})
            raise
        return InsightResponse.from_payload(data)

    def ask(self, req: InsightAskRequest) -> InsightResponse:
        body = req.model_dump(exclude_none=True)
        try:
            data = self._post("/insight/ask", body)
        except httpx.HTTPError as e:
            logger.exception("insight_ask_failed", extra={"error": str(e)})
            raise
        return InsightResponse.from_payload(data)

    def summary(self, req: InsightSummaryRequest | None = None) -> InsightResponse:
        body = (req or InsightSummaryRequest()).model_dump()
        try:
            data = self._post("/insight/summary", body)
        except httpx.HTTPError as e:
            logger.exception("insight_summary_failed", extra={"error": str(e)})
            raise
        return InsightResponse.from_payload(data)
