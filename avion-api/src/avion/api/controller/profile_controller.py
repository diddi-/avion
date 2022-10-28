from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, Api

from avion.api.decorator.with_profile import with_profile
from avion.api.schema.private_profile_schema import PrivateProfileSchema

from avion.domain.service.profile.model.profile import Profile

namespace = Namespace("profile")


@namespace.route("")
class ProfileController(Resource):  # type: ignore
    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api

    @namespace.response(200, "OK",
                        PrivateProfileSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(PrivateProfileSchema.as_namespace_model(namespace))  # type: ignore
    @jwt_required()  # type: ignore
    @with_profile()
    def get(self, profile: Profile) -> Profile:
        # This may look strange but thanks to @with_profile() we've already loaded all details,
        # no need to fetch it again!
        return profile
