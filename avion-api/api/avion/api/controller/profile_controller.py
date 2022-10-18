from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, Api

from avion.api.decorator.with_profile import with_profile
from avion.service.profile.model.profile import Profile
from avion.service.profile.profile_service import ProfileService
from avion.api.schema.private_profile_schema import PrivateProfileSchema

namespace = Namespace("profile")


@namespace.route("")
class ProfilesController(Resource):  # type: ignore
    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api
        self.profile_service = ProfileService()

    @namespace.response(200, "OK",
                        PrivateProfileSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(PrivateProfileSchema.as_namespace_model(namespace))  # type: ignore
    @jwt_required()  # type: ignore
    @with_profile()
    def get(self, profile: Profile) -> Profile:
        return profile
