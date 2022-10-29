from http import HTTPStatus
from typing import cast, Dict, Any, List, Tuple

from avion.api.http_exception import HttpException
from avion.api.input.schema.create_profile_schema import CreateProfileSchema
from avion.api.schema.private_profile_schema import PrivateProfileSchema
from wsgi.di.container import Container
from avion.domain.service.profile.exceptions.duplicate_profile_exception import DuplicateProfileException
from avion.domain.service.profile.model.create_profile_params import CreateProfileParams
from avion.domain.service.profile.model.profile import Profile
from avion.domain.service.profile.profile_service import ProfileService
from avion.domain.service.session.http_session import HttpSession
from flask import request, current_app
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, Api
from marshmallow import ValidationError

namespace = Namespace("profiles")


@namespace.route("")
class ProfilesController(Resource):  # type: ignore
    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api
        container = cast(Container, current_app.config["DIContainer"])
        self.profile_service = container.get_instance(ProfileService)
        self.http_session = container.get_instance(HttpSession)

    @namespace.expect(CreateProfileSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.response(201, "Created",
                        PrivateProfileSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(PrivateProfileSchema.as_namespace_model(namespace))  # type: ignore
    @jwt_required()  # type: ignore
    def post(self) -> Tuple[Profile, int]:
        data = cast(Dict[str, Any], request.json)
        try:
            params = cast(CreateProfileParams, CreateProfileSchema().load(data))
            params.owner_id = self.http_session.get_current_user().id
            return self.profile_service.create_profile(params), 201
        except (ValidationError, DuplicateProfileException) as e:
            raise HttpException(HTTPStatus.BAD_REQUEST, str(e)) from e

    @namespace.response(200, "OK",
                        PrivateProfileSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(PrivateProfileSchema.as_namespace_model(namespace))  # type: ignore
    @jwt_required()  # type: ignore
    def get(self) -> List[Profile]:
        return self.profile_service.get_profiles(self.http_session.get_current_user().id)
