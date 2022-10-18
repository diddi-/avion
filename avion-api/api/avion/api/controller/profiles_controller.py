from typing import cast, Dict, Any, List

from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, Api

from avion.api.input.schema.create_profile_schema import CreateProfileSchema
from avion.api.schema.profile_schema import ProfileSchema
from avion.service.profile.model.profile import Profile
from avion.service.profile.model.create_profile_params import CreateProfileParams
from avion.service.profile.profile_service import ProfileService
from avion.service.session.http_session import HttpSession

namespace = Namespace("profiles")


@namespace.route("")
class ProfilesController(Resource):  # type: ignore
    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api
        self.profile_service = ProfileService()
        self.http_session = HttpSession()

    @namespace.expect(CreateProfileSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.response(200, "Created",
                        ProfileSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(ProfileSchema.as_namespace_model(namespace))  # type: ignore
    @jwt_required()  # type: ignore
    def post(self) -> Profile:
        data = cast(Dict[str, Any], request.json)
        params = cast(CreateProfileParams, CreateProfileSchema().load(data))
        params.owner_id = self.http_session.get_current_user().id
        return self.profile_service.create_profile(params)

    @namespace.response(200, "Created",
                        ProfileSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(ProfileSchema.as_namespace_model(namespace))  # type: ignore
    @jwt_required()  # type: ignore
    def get(self) -> List[Profile]:
        return self.profile_service.get_profiles(self.http_session.get_current_user().id)
