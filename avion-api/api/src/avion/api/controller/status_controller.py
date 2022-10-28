from wsgi.controller.controller import Controller
from wsgi.controller.controller_result import ControllerResult
from wsgi.middleware.router.route import Route


class StatusController(Controller):

    @Route()
    def get(self) -> ControllerResult:
        return ControllerResult("{'status': 'ok'}")
