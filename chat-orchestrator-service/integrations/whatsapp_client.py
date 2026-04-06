import logging

import httpx

from app.config.settings import Settings
from app.schemas.message_schema import OutgoingWhatsApp

logger = logging.getLogger(__name__)


class WhatsAppClient:
    """Meta Cloud API: send text messages."""

    def __init__(self, settings: Settings) -> None:
        self._token = settings.whatsapp_api_token
        self._phone_id = settings.whatsapp_phone_number_id
        self._version = settings.whatsapp_api_version
        self._graph = settings.whatsapp_graph_base.rstrip("/")

    def send(self, outgoing: OutgoingWhatsApp) -> None:
        if not self._token or not self._phone_id:
            logger.warning(
                "whatsapp_not_configured",
                extra={"to": outgoing.to, "preview": outgoing.message[:80]},
            )
            return
        url = f"{self._graph}/{self._version}/{self._phone_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": outgoing.to.lstrip("+"),
            "type": "text",
            "text": {"body": outgoing.message[:4096]},
        }
        headers = {"Authorization": f"Bearer {self._token}"}
        with httpx.Client(timeout=30.0) as client:
            r = client.post(url, json=payload, headers=headers)
            r.raise_for_status()
