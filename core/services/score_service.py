from injector import inject
from core.services.log_service import LogService
from core.services.service_base import ServiceBase
from settings import Settings


class ScoreService(ServiceBase):
    @inject
    def __init__(self, log_service: LogService, settings: Settings):
        super().__init__(settings)
        self.services.logger = log_service

        # Notify that the service is initialized
        self.events.on_service_initialized.notify()
