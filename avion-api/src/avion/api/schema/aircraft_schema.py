from flask_restx import Namespace, OrderedModel, fields as restx_fields


class AircraftSchema:
    @staticmethod
    def as_namespace_model(namespace: Namespace) -> OrderedModel:
        return namespace.model("aircraft", {
            "id": restx_fields.Integer(required=True),
            "model_id": restx_fields.Integer(required=True),
            "company_id": restx_fields.Integer(required=True),
            "registration": restx_fields.String(),
            "purchased_at": restx_fields.String()
        })
