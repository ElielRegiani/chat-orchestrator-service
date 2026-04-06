"""Optional direct ML Service integration — stub for future use."""

from app.config.settings import Settings


class MLServiceClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
