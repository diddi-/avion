from typing import cast, List

from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, Api

from avion.api.decorator.with_profile import with_profile
from avion.api.schema.company_schema import CompanySchema
from avion.api.input.schema.create_company_params_schema import CreateCompanyParamsSchema
from avion.service.company.model.company import Company
from avion.service.company.model.create_company_params import CreateCompanyParams
from avion.service.company.repository.company_repository import CompanyRepository
from avion.service.company.company_service import CompanyService
from avion.service.profile.model.profile import Profile
from avion.service.session.http_session import HttpSession

namespace = Namespace("company")


@namespace.route("")
class CompanyController(Resource):  # type: ignore
    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api
        self.company_service = CompanyService()
        self.http_session = HttpSession()

    @namespace.expect(CreateCompanyParamsSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.response(200, "Created",
                        CompanySchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(CompanySchema.as_namespace_model(namespace))  # type: ignore
    @jwt_required()  # type: ignore
    @with_profile()
    def post(self, profile: Profile) -> Company:
        data = request.json
        params = cast(CreateCompanyParams, CreateCompanyParamsSchema().load(data))  # type: ignore
        return self.company_service.create_company(profile, params)

    @namespace.response(200, "OK", CompanySchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(CompanySchema.as_namespace_model(namespace))  # type: ignore
    def get(self) -> List[Company]:
        companies = CompanyRepository().get_all_companies()
        return companies
