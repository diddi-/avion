from flask_restx import Namespace, OrderedModel, fields as restx_fields


class ProfileSchema:
    @staticmethod
    def as_namespace_model(namespace: Namespace) -> OrderedModel:
        return namespace.model("profile", {
            "id": restx_fields.Integer(required=True),
            "created_at": restx_fields.DateTime(required=True, dt_format="iso8601"),
            "firstname": restx_fields.String(required=True),
            "lastname": restx_fields.String(required=True),
        })
