from http import HTTPStatus
from typing import cast, Dict, Any, Tuple

from flask import request, current_app
from flask_restx import Namespace, Resource, Api
from marshmallow import ValidationError

from avion.api.http_exception import HttpException
from avion.api.input.schema.create_user_account_params_schema import CreateUserAccountParamsSchema
from avion.api.schema.user_account_schema import UserAccountSchema
from avion.domain.service.account.exceptions.duplicate_account_exception import DuplicateAccountException
from avion.domain.service.account.model.create_user_account_params import CreateUserAccountParams
from avion.domain.service.account.model.user_account import UserAccount
from avion.domain.service.account.user_account_service import UserAccountService
from wsgi.di.container import Container

namespace = Namespace("user_account")


@namespace.route("")
class UserAccountController(Resource):  # type: ignore
    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api
        container = cast(Container, current_app.config["DIContainer"])
        self.user_account_service = container.get_instance(UserAccountService)

    @namespace.expect(CreateUserAccountParamsSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.response(201, "Created",
                        UserAccountSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(UserAccountSchema.as_namespace_model(namespace))  # type: ignore
    def post(self) -> Tuple[UserAccount, int]:
        data = cast(Dict[str, Any], request.json)
        try:
            params = cast(CreateUserAccountParams, CreateUserAccountParamsSchema().load(data))
            user = self.user_account_service.register(params)
        except (ValidationError, DuplicateAccountException) as e:
            raise HttpException(HTTPStatus.BAD_REQUEST, str(e)) from e
        return user, 201
