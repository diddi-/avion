from flask_restx import Namespace, OrderedModel, fields as restx_fields
from marshmallow import post_load, Schema, fields

from avion.parameters.create_airline_params import CreateAirlineParams


class CreateAirlineParamsSchema(Schema):
    name = fields.String(required=True)
    owner_id = fields.Integer(required=True)

    @staticmethod
    def as_namespace_model(namespace: Namespace) -> OrderedModel:
        return namespace.model("airline", {
            "name": restx_fields.String(required=True),
            "owner_id": restx_fields.Integer(required=True),
        })

    @post_load
    def to_obj(self, data, **_) -> CreateAirlineParams:  # type: ignore
        return CreateAirlineParams(data["name"], data["owner_id"])
