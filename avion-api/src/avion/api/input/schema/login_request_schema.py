from avion.domain.service.account.model.login_request import LoginRequest
from flask_restx import Namespace, OrderedModel, fields as restx_fields
from marshmallow import post_load, Schema, fields


class LoginRequestSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    @staticmethod
    def as_namespace_model(namespace: Namespace) -> OrderedModel:
        return namespace.model("user-account", {
            "username": restx_fields.String(),
            "password": restx_fields.String(),
        })

    @post_load
    def to_obj(self, data, **_) -> LoginRequest:  # type: ignore
        return LoginRequest(data["username"], data["password"])
