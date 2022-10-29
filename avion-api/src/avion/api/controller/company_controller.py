from http import HTTPStatus
from typing import cast, List, Tuple

from flask import request, current_app
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, Api
from marshmallow import ValidationError

from avion.api.decorator.with_profile import with_profile
from avion.api.http_exception import HttpException
from avion.api.input.schema.create_company_params_schema import CreateCompanyParamsSchema
from avion.api.schema.company_schema import CompanySchema
from avion.domain.di.container import Container
from avion.domain.service.company.company_service import CompanyService
from avion.domain.service.company.exceptions.duplicate_company_exception import DuplicateCompanyException
from avion.domain.service.company.model.company import Company
from avion.domain.service.company.model.create_company_params import CreateCompanyParams
from avion.domain.service.company.repository.company_repository import CompanyRepository
from avion.domain.service.profile.model.profile import Profile
from avion.domain.service.session.http_session import HttpSession

namespace = Namespace("company")


@namespace.route("")
class CompanyController(Resource):  # type: ignore
    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api
        container = cast(Container, current_app.config["DIContainer"])
        self.company_service = container.get_instance(CompanyService)
        self.http_session = container.get_instance(HttpSession)

    @namespace.expect(CreateCompanyParamsSchema.as_namespace_model(namespace))  # type: ignore
    @namespace.response(HTTPStatus.CREATED, "Created",
                        CompanySchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(CompanySchema.as_namespace_model(namespace))  # type: ignore
    @jwt_required()  # type: ignore
    @with_profile()
    def post(self, profile: Profile) -> Tuple[Company, int]:
        data = request.json
        try:
            params = cast(CreateCompanyParams, CreateCompanyParamsSchema().load(data))  # type: ignore
            return self.company_service.create_company(profile, params), HTTPStatus.CREATED
        except (ValidationError, DuplicateCompanyException) as e:
            raise HttpException(HTTPStatus.BAD_REQUEST, str(e)) from e

    @namespace.response(HTTPStatus.OK, "OK", CompanySchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(CompanySchema.as_namespace_model(namespace))  # type: ignore
    def get(self) -> List[Company]:
        companies = CompanyRepository().get_all_companies()
        return companies
