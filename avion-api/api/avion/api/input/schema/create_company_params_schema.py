from flask_restx import Namespace, OrderedModel, fields as restx_fields
from marshmallow import post_load, Schema, fields

from avion.service.company.model.create_company_params import CreateCompanyParams


class CreateCompanyParamsSchema(Schema):
    name = fields.String(required=True)

    @staticmethod
    def as_namespace_model(namespace: Namespace) -> OrderedModel:
        return namespace.model("company", {
            "name": restx_fields.String(required=True),
        })

    @post_load
    def to_obj(self, data, **_) -> CreateCompanyParams:  # type: ignore
        return CreateCompanyParams(data["name"])
