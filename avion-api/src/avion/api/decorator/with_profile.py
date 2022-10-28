from functools import wraps
from http import HTTPStatus
from typing import Callable, TypeVar, cast

from avion.api.http_exception import HttpException
from avion.domain.di.container import Container
from avion.domain.service.profile.profile_service import ProfileService
from avion.domain.service.session.http_session import HttpSession
from flask import request, current_app

T = TypeVar("T")
FunctionSpec = Callable[..., T]


def with_profile() -> Callable[[FunctionSpec[T]], FunctionSpec[T]]:
    """ This decorator will pass a Profile object as the first argument to a controller method.
        Example:
             class Controller(Resource):
                @with_profile()
                def get(self, profile: Profile):
                   ...
            """

    def decorator(func: FunctionSpec[T]) -> FunctionSpec[T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:  # type: ignore
            container = cast(Container, current_app.config["DIContainer"])
            http = container.get_instance(HttpSession)
            profile_service = container.get_instance(ProfileService)
            user = http.get_current_user()
            header_name = "X-PROFILE-ID"
            if header_name not in request.headers:
                raise HttpException(HTTPStatus.BAD_REQUEST, f"Missing required {header_name}. {request.headers.keys()}")

            profile_id = int(request.headers[header_name])
            assert user.id is not None  # Mypy..
            if not profile_service.account_has_profile(user.id, profile_id):
                raise HttpException(HTTPStatus.UNAUTHORIZED, "You do not have access to this profile")

            return func(args[0], profile_service.get_profile(profile_id), *args[1:], **kwargs)

        return wrapper

    return decorator
