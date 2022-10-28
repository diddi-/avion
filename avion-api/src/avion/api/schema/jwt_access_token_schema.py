from flask_restx import Namespace, OrderedModel, fields as restx_fields


class JwtAccessTokenSchema:
    @staticmethod
    def as_namespace_model(namespace: Namespace) -> OrderedModel:
        return namespace.model("jwt-access-token", {
            "sub": restx_fields.String(),
            "iss": restx_fields.String(),
        })
