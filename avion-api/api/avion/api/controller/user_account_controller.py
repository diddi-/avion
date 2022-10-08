from typing import cast, Dict, Any

from flask import request
from flask_restx import Namespace, Resource, Api

from avion.api.input.schema.create_user_account_params_schema import CreateUserAccountParamsSchema
from avion.api.schema.user_account_schema import UserAccountSchema
from avion.service.account.model.user_account import UserAccount
from avion.service.account.model.create_user_account_params import CreateUserAccountParams
from avion.service.account.user_account_service import UserAccountService

namespace = Namespace("user_account")


@namespace.route("")
class UserAccountController(Resource):  # type: ignore
    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api
        self.user_account_service = UserAccountService()

    @namespace.expect(CreateUserAccountParamsSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.response(200, "Created",
                        UserAccountSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(UserAccountSchema.as_namespace_model(namespace))  # type: ignore
    def post(self) -> UserAccount:
        data = cast(Dict[str, Any], request.json)
        params = cast(CreateUserAccountParams, CreateUserAccountParamsSchema().load(data))
        return self.user_account_service.register(params)
