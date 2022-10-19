from typing import cast, Dict, Any

from flask import request
from flask_restx import Namespace, Resource, Api
from flask_restx._http import HTTPStatus

from avion.api.http_exception import HttpException
from avion.api.input.schema.login_request_schema import LoginRequestSchema
from avion.api.schema.login_response_schema import LoginResponseSchema
from avion.service.account.exceptions.login_failed_exception import LoginFailedException
from avion.service.account.model.login_request import LoginRequest
from avion.service.account.model.login_response import LoginResponse
from avion.service.account.user_account_service import UserAccountService

namespace = Namespace("login")


@namespace.route("")
class LoginController(Resource):  # type: ignore
    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api
        self.user_account_service = UserAccountService()

    @namespace.expect(LoginRequestSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.response(200, "Created",
                        LoginResponseSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(LoginResponseSchema.as_namespace_model(namespace))  # type: ignore
    def post(self) -> LoginResponse:
        data = cast(Dict[str, Any], request.json)
        login_request = cast(LoginRequest, LoginRequestSchema().load(data))
        try:
            return self.user_account_service.login(login_request)
        except LoginFailedException as e:
            raise HttpException(HTTPStatus.UNAUTHORIZED, str(e)) from e
