from flask_restx import Namespace, OrderedModel, fields as restx_fields
from marshmallow import post_load, Schema, fields

from avion.api.input.create_airline_params import CreateAirlineParams


class CreateAirlineParamsSchema(Schema):
    name = fields.String(required=True)

    @staticmethod
    def as_namespace_model(namespace: Namespace) -> OrderedModel:
        return namespace.model("airline", {
            "name": restx_fields.String()
        })

    @post_load
    def to_obj(self, data, **_) -> CreateAirlineParams:  # type: ignore
        return CreateAirlineParams(data["name"])
