from avion.domain.service.status.model.status import Status


class StatusService:
    def get_status(self) -> Status:
        return Status("OK")
