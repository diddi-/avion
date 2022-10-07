from flask_restx import Namespace, OrderedModel, fields as restx_fields
from marshmallow import post_load, Schema, fields

from avion.parameters.create_profile_params import CreateProfileParams


class CreateProfileSchema(Schema):
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)

    @staticmethod
    def as_namespace_model(namespace: Namespace) -> OrderedModel:
        return namespace.model("profile", {
            "firstname": restx_fields.String(),
            "lastname": restx_fields.String()
        })

    @post_load
    def to_obj(self, data, **_) -> CreateProfileParams:  # type: ignore
        return CreateProfileParams(data["firstname"], data["lastname"])
