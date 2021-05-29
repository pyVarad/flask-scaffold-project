import toml
from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_log_request_id import RequestID, current_request_id

from resources.users import UserResource, UsersResource
from logger import initialize_logging

app = Flask(__name__)


def create_app(config):
    app.config.from_file('config/dev.toml', load=toml.load)
    api = Api(app)
    RequestID(app)
    initialize_logging()

    swagger_blueprint = get_swaggerui_blueprint(
        app.config['SWAGGER_URL'],
        app.config['SWAGGER_API_URL'],
        config = {
            'app_name': 'Workbench Application'
        }
    )    

    api.add_resource(UserResource, '/user/<string:userId>')
    api.add_resource(UsersResource, '/users')
    app.register_blueprint(swagger_blueprint, url_prefix=app.config['SWAGGER_API_URL'])

    return app

@app.after_request
def append_request_id(response):
    response.headers.add('X-REQUEST-ID', current_request_id())
    return response