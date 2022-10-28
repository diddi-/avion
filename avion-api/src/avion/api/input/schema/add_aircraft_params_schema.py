from avion.domain.service.fleet.model.add_aircraft_params import AddAircraftParams
from flask_restx import Namespace, OrderedModel, fields as restx_fields
from marshmallow import post_load, Schema, fields


class AddAircraftParamsSchema(Schema):
    company_id = fields.Integer(required=True)
    aircraft_model_id = fields.Integer(required=True)

    @staticmethod
    def as_namespace_model(namespace: Namespace) -> OrderedModel:
        return namespace.model("add-aircraft", {
            "company_id": restx_fields.Integer(),
            "aircraft_model_id": restx_fields.Integer()
        })

    @post_load
    def to_obj(self, data, **_) -> AddAircraftParams:  # type: ignore
        return AddAircraftParams(int(data["company_id"]), int(data["aircraft_model_id"]))
