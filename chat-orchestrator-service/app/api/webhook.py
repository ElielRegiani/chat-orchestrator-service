from functools import lru_cache

from fastapi import APIRouter, HTTPException

from app.config.settings import get_settings
from app.schemas.message_schema import OutgoingWhatsApp, WebhookIn
from app.services.chat_service import ChatService
from app.services.orchestrator import Orchestrator
from integrations.insight_service_client import InsightServiceClient
from integrations.whatsapp_client import WhatsAppClient

router = APIRouter()


@lru_cache
def _chat_service() -> ChatService:
    s = get_settings()
    return ChatService(
        orchestrator=Orchestrator(InsightServiceClient(s)),
        whatsapp=WhatsAppClient(s),
    )


@router.post("/webhook", response_model=OutgoingWhatsApp)
def webhook(payload: WebhookIn) -> OutgoingWhatsApp:
    try:
        return _chat_service().process_webhook_payload(payload.model_dump(by_alias=True))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
