from functools import wraps
from typing import Callable, TypeVar

from flask import request

from avion.service.profile.profile_service import ProfileService
from avion.service.session.http_session import HttpSession

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
            user = HttpSession().get_current_user()
            header_name = "X-PROFILE-ID"
            if header_name not in request.headers:
                raise ValueError(f"Missing required {header_name}. {request.headers.keys()}")

            profile_id = int(request.headers[header_name])
            assert user.id is not None  # Mypy..
            if not ProfileService().account_has_profile(user.id, profile_id):
                raise ValueError("You do not have access to this profile")

            return func(args[0], ProfileService().get_profile(profile_id), *args[1:], **kwargs)

        return wrapper

    return decorator
