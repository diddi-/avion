from flask_restx import Namespace, OrderedModel, fields as restx_fields


class LoginResponseSchema:
    @staticmethod
    def as_namespace_model(namespace: Namespace) -> OrderedModel:
        return namespace.model("login-response", {
            "token": restx_fields.String(required=True),
        })
