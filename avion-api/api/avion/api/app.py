from flask import Flask
from flask_restx import Api

from avion.api.controller.airline_controller import namespace as airline_namespace
from avion.api.controller.airline_name_controller import namespace as airline_name_namespace
from avion.api.controller.status_controller import namespace as status_namespace
from avion.api.controller.user_account_controller import namespace as account_namespace


def create_app() -> Flask:
    """ Flask app factory function, automatically called by 'flask run' command.
    https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/ """
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    api = Api(app)
    api.add_namespace(status_namespace, "/status")
    api.add_namespace(airline_namespace, "/airline")
    api.add_namespace(airline_name_namespace, "/airline")
    api.add_namespace(account_namespace, "/account")

    return app
