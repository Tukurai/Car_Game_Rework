from datetime import datetime
from injector import inject
from core.enums.log_level import LogLevel
from core.services.service_base import ServiceBase
from settings import Settings


class LogService(ServiceBase):
    """Service for logging messages to the console, or a file."""

    @inject
    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.history = []

    def log(self, message: str, log_level: LogLevel = LogLevel.INFO):
        """Log a message to the console, or a file."""
        if Settings.LOG_LEVEL.value <= log_level.value:
            print(
                f"{log_level} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {message}"
            )
        self.history.append(
            (
                log_level,
                datetime.now(),
                f"{log_level} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {message}",
            )
        )
