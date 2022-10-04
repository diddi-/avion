from flask_restx import Namespace, Resource, Api

from avion.api.schema.airline_schema import AirlineSchema
from avion.model.airline import Airline
from avion.repository.airline_repository import AirlineRepository

namespace = Namespace("airline")


@namespace.route("/<string:name>")
class AirlineNameController(Resource):  # type: ignore
    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api

    @namespace.response(200, "Airline fetched", AirlineSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(AirlineSchema.as_namespace_model(namespace))  # type: ignore
    def get(self, name: str) -> Airline:
        return AirlineRepository().get_airline_by_name(name)
