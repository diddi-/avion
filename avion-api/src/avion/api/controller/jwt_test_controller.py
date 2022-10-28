from typing import Dict, Any

from avion.api.decorator.with_profile import with_profile
from avion.api.schema.jwt_access_token_schema import JwtAccessTokenSchema
from avion.domain.service.account.model.jwt_access_token import JwtAccessToken
from avion.domain.service.account.user_account_service import UserAccountService
from avion.domain.service.profile.model.profile import Profile
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, Api

namespace = Namespace("jwt-test")


@namespace.route("")
class JwtTestController(Resource):  # type: ignore
    """ Simple JWT Token test/verification controller. This is not intended for production use but rather
    a simple means of understanding and learning about JWT tokens. Can be safely removed. """

    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api
        self.user_account_service = UserAccountService()

    @namespace.response(200, "Created",
                        JwtAccessTokenSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(JwtAccessTokenSchema.as_namespace_model(namespace))  # type: ignore
    @jwt_required()  # type: ignore
    def post(self) -> JwtAccessToken:
        authz = request.headers.get("Authorization")
        if authz is None:
            raise ValueError("Missing Authorization header")
        return self.user_account_service.parse_token(authz.split(" ")[1])

    @jwt_required()  # type: ignore
    @with_profile()
    def get(self, profile: Profile) -> Dict[str, Any]:
        return {"Profile": profile.firstname}
