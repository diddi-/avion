from flask_restx import Namespace, OrderedModel, fields as restx_fields


class StatusSchema:
    @staticmethod
    def as_namespace_model(namespace: Namespace) -> OrderedModel:
        return namespace.model("status", {
            "status": restx_fields.String(required=True),
        })
