from avion.domain.service.status.status_service import StatusService
from wsgi.controller.controller import Controller
from wsgi.controller.controller_result import ControllerResult
from wsgi.middleware.router.route import Route


class StatusController(Controller):

    def __init__(self, service: StatusService) -> None:
        super().__init__()
        self.service = service

    @Route()
    def get(self) -> ControllerResult:
        return ControllerResult(f'{"status":"{self.service.get_status().status}"}')
