from typing import cast

from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, Api

from avion.api.decorator.with_profile import with_profile
from avion.api.input.schema.add_aircraft_params_schema import AddAircraftParamsSchema
from avion.api.schema.aircraft_schema import AircraftSchema
from avion.domain.service.fleet.fleet_service import FleetService
from avion.domain.service.fleet.model.add_aircraft_params import AddAircraftParams
from avion.domain.service.fleet.model.aircraft import Aircraft
from avion.domain.service.profile.model.profile import Profile

namespace = Namespace("fleet")


@namespace.route("")
class FleetController(Resource):  # type: ignore
    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api
        self.fleet_service = FleetService()

    @namespace.expect(AddAircraftParamsSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.response(200, "Created",
                        AircraftSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(AircraftSchema.as_namespace_model(namespace))  # type: ignore
    @jwt_required()  # type: ignore
    @with_profile()
    def post(self, profile: Profile) -> Aircraft:
        data = request.json
        params = cast(AddAircraftParams, AddAircraftParamsSchema().load(data))  # type: ignore
        return self.fleet_service.buy_aircraft(profile, params.company_id, params.aircraft_model_id)
