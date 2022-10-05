from flask_restx import Namespace, OrderedModel, fields as restx_fields


class UserAccountSchema:
    @staticmethod
    def as_namespace_model(namespace: Namespace) -> OrderedModel:
        return namespace.model("user-account", {
            "id": restx_fields.Integer(required=True),
            "created-at": restx_fields.DateTime(required=True, dt_format="iso8601", attribute="created_at"),
            "firstname": restx_fields.String(required=True),
            "lastname": restx_fields.String(required=True),
            "email": restx_fields.String(required=True),
        })
