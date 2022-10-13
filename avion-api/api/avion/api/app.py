import json

from flask import Flask, Response
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api


from avion.api.controller.company_controller import namespace as company_namespace
from avion.api.controller.company_name_controller import namespace as company_name_namespace
from avion.api.controller.jwt_test_controller import namespace as jwt_test_namespace
from avion.api.controller.login_controller import namespace as login_namespace
from avion.api.controller.status_controller import namespace as status_namespace
from avion.api.controller.user_account_controller import namespace as account_namespace
from avion.api.controller.profile_controller import namespace as profile_namespace
from avion.api.controller.fleet_controller import namespace as fleet_namespace
from avion.config.config import current_config


def create_app() -> Flask:
    """ Flask app factory function, automatically called by 'flask run' command.
    https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/ """
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    api = Api(app)
    current_config.load()
    app.config["JWT_SECRET_KEY"] = current_config.jwt.secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = current_config.jwt.access_token_lifetime
    app.config["JWT_DECODE_ISSUER"] = current_config.jwt.issuer
    app.config["JWT_ENCODE_ISSUER"] = current_config.jwt.issuer
    JWTManager(app)
    CORS(app)

    api.add_namespace(status_namespace, "/status")
    api.add_namespace(company_namespace, "/company")
    api.add_namespace(company_name_namespace, "/company")
    api.add_namespace(account_namespace, "/account")
    api.add_namespace(login_namespace, "/login")
    api.add_namespace(jwt_test_namespace, "/token")
    api.add_namespace(profile_namespace, "/profile")
    api.add_namespace(fleet_namespace, "/fleet")

    # @app.errorhandler(Exception)
    # def handle_exception(e: Exception) -> Response:
    #     """Return JSON instead of HTML for HTTP errors."""
    #     body = json.dumps({
    #         "error": e.__class__.__name__,
    #         "description": str(e),
    #     })
    #     response = app.make_response((body, 500, ))
    #     response.headers.add("Content-Type", "application/json")
    #     return response

    return app
