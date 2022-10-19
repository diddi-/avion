from flask import Flask, g

from avion.di.container import Container
from avion.service.account.repository.user_account_repository import UserAccountRepository
from avion.service.account.user_account_service import UserAccountService


class FlaskContainer:
    """
    This class ensures that a Flask app context comes with a container when a request is made.
    """

    def __init__(self, app: Flask):
        self._container = Container()
        self._container.resolve(UserAccountService).using(UserAccountService)
        self._container.resolve(UserAccountRepository).using(UserAccountRepository)


        @app.before_request
        def _add_default_container_if_none_set() -> None:
            # This conditional is very important! Tests that want to insert their stubbed container
            # can only replace the container before this hook is executed.
            if not hasattr(g, "container"):
                setattr(g, "container", self._container)
