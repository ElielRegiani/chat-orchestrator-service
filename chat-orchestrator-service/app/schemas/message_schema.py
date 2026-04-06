from enum import Enum

from pydantic import BaseModel, Field


class Intent(str, Enum):
    CONSULT_ASSET = "CONSULT_ASSET"
    ASK_RECOMMENDATION = "ASK_RECOMMENDATION"
    MARKET_SUMMARY = "MARKET_SUMMARY"
    UNKNOWN = "UNKNOWN"


class WebhookIn(BaseModel):
    from_: str = Field(..., alias="from", description="WhatsApp user phone (E.164 without +)")
    message: str = Field(..., min_length=1)

    model_config = {"populate_by_name": True}


class ParsedMessage(BaseModel):
    user_phone: str
    text: str


class OutgoingWhatsApp(BaseModel):
    to: str
    message: str


class InsightExplainRequest(BaseModel):
    ticker: str | None = None
    question: str


class InsightAskRequest(BaseModel):
    question: str
    ticker: str | None = None


class InsightSummaryRequest(BaseModel):
    pass


class InsightResponse(BaseModel):
    """Normalizes Insight Service JSON (answer or text)."""

    text: str = ""

    @classmethod
    def from_payload(cls, data: dict) -> "InsightResponse":
        if not data:
            return cls(text="")
        text = data.get("answer") or data.get("text") or data.get("message") or ""
        if isinstance(text, dict):
            text = str(text)
        return cls(text=str(text).strip())
