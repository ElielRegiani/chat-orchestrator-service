from app.schemas.message_schema import InsightResponse, OutgoingWhatsApp

_FALLBACK = "Não entendi sua pergunta. Pode reformular?"


def build_whatsapp_reply(user_phone: str, insight: InsightResponse) -> OutgoingWhatsApp:
    body = insight.text.strip() if insight.text else ""
    if not body:
        body = _FALLBACK
    return OutgoingWhatsApp(to=user_phone, message=body)
