from flask_restx import Namespace, OrderedModel, fields as restx_fields


class AirlineSchema:
    @staticmethod
    def as_namespace_model(namespace: Namespace) -> OrderedModel:
        return namespace.model("airline", {
            "id": restx_fields.Integer(required=True),
            "created-at": restx_fields.DateTime(required=True, dt_format="iso8601", attribute="created_at"),
            "name": restx_fields.String(required=True),
        })
