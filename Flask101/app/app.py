import os
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
    db.init_app(app)
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


@app.before_first_request
def create_db():
    db.create_all()


@app.after_request
def append_request_id(response):
    response.headers.add('X-REQUEST-ID', current_request_id())
    return response


if __name__ == "__main__":
    from db import db
    app_config = os.getenv('APP_CONFIG', 'config/dev.toml')
    create_app(app_config)
    app.run(port=5000, debug=True)