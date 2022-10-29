from typing import cast, Dict, Any

from avion.api.http_exception import HttpException
from avion.api.input.schema.login_request_schema import LoginRequestSchema
from avion.api.schema.login_response_schema import LoginResponseSchema
from wsgi.di.container import Container
from avion.domain.service.account.exceptions.login_failed_exception import LoginFailedException
from avion.domain.service.account.model.login_request import LoginRequest
from avion.domain.service.account.model.login_response import LoginResponse
from avion.domain.service.account.user_account_service import UserAccountService
from flask import request, current_app
from flask_restx import Namespace, Resource, Api
from flask_restx._http import HTTPStatus
from marshmallow import ValidationError

namespace = Namespace("login")


@namespace.route("")
class LoginController(Resource):  # type: ignore
    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api
        self.container = cast(Container, current_app.config["DIContainer"])
        self.user_account_service = self.container.get_instance(UserAccountService)

    @namespace.expect(LoginRequestSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.response(200, "OK",
                        LoginResponseSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(LoginResponseSchema.as_namespace_model(namespace))  # type: ignore
    def post(self) -> LoginResponse:
        data = cast(Dict[str, Any], request.json)
        try:
            login_request = cast(LoginRequest, LoginRequestSchema().load(data))
        except ValidationError as e:
            raise HttpException(HTTPStatus.BAD_REQUEST, str(e)) from e

        try:
            return self.user_account_service.login(login_request)
        except LoginFailedException as e:
            raise HttpException(HTTPStatus.UNAUTHORIZED, str(e)) from e
