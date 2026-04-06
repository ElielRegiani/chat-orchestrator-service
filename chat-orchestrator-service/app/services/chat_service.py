import logging
import time
from typing import Any

from app.schemas.message_schema import Intent, OutgoingWhatsApp, ParsedMessage, WebhookIn
from app.services.intent_detector import detect_intent
from app.services.orchestrator import Orchestrator
from app.services.response_builder import build_whatsapp_reply
from integrations.whatsapp_client import WhatsAppClient

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(
        self,
        orchestrator: Orchestrator,
        whatsapp: WhatsAppClient,
    ) -> None:
        self._orchestrator = orchestrator
        self._whatsapp = whatsapp

    def parse_webhook(self, body: WebhookIn) -> ParsedMessage:
        return ParsedMessage(user_phone=body.from_, text=body.message.strip())

    def process(self, parsed: ParsedMessage) -> OutgoingWhatsApp:
        started = time.perf_counter()
        intent = detect_intent(parsed.text)
        insight = self._orchestrator.run(intent, parsed.text)
        out = build_whatsapp_reply(parsed.user_phone, insight)
        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.info(
            "chat_message_processed",
            extra={
                "intent": intent.value,
                "latency_ms": round(elapsed_ms, 2),
                "metrics": True,
            },
        )
        self._whatsapp.send(out)
        return out

    def process_webhook_payload(self, payload: dict[str, Any]) -> OutgoingWhatsApp:
        body = WebhookIn.model_validate(payload)
        parsed = self.parse_webhook(body)
        return self.process(parsed)
