from typing import cast, List

from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, Api

from avion.api.input.schema.create_airline_params_schema import CreateAirlineParamsSchema
from avion.api.schema.airline_schema import AirlineSchema
from avion.model.airline import Airline
from avion.parameters.create_airline_params import CreateAirlineParams
from avion.repository.airline_repository import AirlineRepository
from avion.service.company.company_service import CompanyService
from avion.service.session.http_session import HttpSession

namespace = Namespace("airline")


@namespace.route("")
class AirlineController(Resource):  # type: ignore
    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api
        self.company_service = CompanyService()
        self.http_session = HttpSession()

    @namespace.expect(CreateAirlineParamsSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.response(200, "Created",
                        AirlineSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(AirlineSchema.as_namespace_model(namespace))  # type: ignore
    @jwt_required()
    def post(self) -> Airline:
        data = request.json
        params = cast(CreateAirlineParams, CreateAirlineParamsSchema().load(data))  # type: ignore
        return self.company_service.create_company(self.http_session.get_current_user().id, params)

    @namespace.response(200, "OK", AirlineSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(AirlineSchema.as_namespace_model(namespace))  # type: ignore
    def get(self) -> List[Airline]:
        airlines = AirlineRepository().get_all_airlines()
        return airlines
