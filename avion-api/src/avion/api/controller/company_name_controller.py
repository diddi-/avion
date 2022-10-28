from avion.api.schema.company_schema import CompanySchema
from avion.domain.service.company.model.company import Company
from avion.domain.service.company.repository.company_repository import CompanyRepository
from flask_restx import Namespace, Resource, Api

namespace = Namespace("company")


@namespace.route("/<string:name>")
class CompanyNameController(Resource):  # type: ignore
    def __init__(self, api: Api):
        super().__init__(api)
        self.api = api

    @namespace.response(200, "Company fetched", CompanySchema.as_namespace_model(namespace))  # type: ignore
    @namespace.marshal_with(CompanySchema.as_namespace_model(namespace))  # type: ignore
    def get(self, name: str) -> Company:
        return CompanyRepository().get_company_by_name(name)
