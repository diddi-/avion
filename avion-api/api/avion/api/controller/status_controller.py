from typing import Dict

from flask_restx import Resource, Api, Namespace

namespace = Namespace("status")


@namespace.route("/")
class StatusController(Resource):  # type: ignore
    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api

    def get(self) -> Dict[str, str]:
        return {"status": "OK"}
