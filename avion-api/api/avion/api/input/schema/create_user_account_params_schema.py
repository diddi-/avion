from flask_restx import Namespace, OrderedModel, fields as restx_fields
from marshmallow import post_load, Schema, fields

from avion.service.account.model.create_user_account_params import CreateUserAccountParams


class CreateUserAccountParamsSchema(Schema):
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)

    @staticmethod
    def as_namespace_model(namespace: Namespace) -> OrderedModel:
        return namespace.model("user-account", {
            "firstname": restx_fields.String(),
            "lastname": restx_fields.String(),
            "email": restx_fields.String(),
        })

    @post_load
    def to_obj(self, data, **_) -> CreateUserAccountParams:  # type: ignore
        return CreateUserAccountParams(data["firstname"], data["lastname"], data["email"],
                                       data["password"])
