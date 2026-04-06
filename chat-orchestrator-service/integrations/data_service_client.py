"""Optional direct Data Service integration — stub for future use."""

from app.config.settings import Settings


class DataServiceClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
