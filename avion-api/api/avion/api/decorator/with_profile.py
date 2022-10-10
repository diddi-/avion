from functools import wraps

from flask import request

from avion.service.profile.profile_service import ProfileService
from avion.service.session.http_session import HttpSession


def with_profile():
    """ This decorator will pass a Profile object as the first argument to a controller method.
        Example:
             class Controller(Resource):
                @with_profile()
                def get(self, profile: Profile):
                   ...
            """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):  # type: ignore
            user = HttpSession().get_current_user()
            header_name = "X-PROFILE-ID"
            if header_name not in request.headers:
                raise ValueError(f"Missing required {header_name}. {request.headers.keys()}")

            profile_id = int(request.headers.get(header_name, None))
            if not ProfileService().account_has_profile(user.id, profile_id):
                raise ValueError("You do not have access to this profile")

            return func(args[0], ProfileService().get_profile(profile_id), *args[1:], **kwargs)

        return wrapper

    return decorator
