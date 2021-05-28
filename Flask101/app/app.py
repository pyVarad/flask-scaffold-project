from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_log_request_id import RequestID, current_request_id

from resources.users import UserResource, UsersResource
from logger import initialize_logging




app = Flask(__name__)

app.config['secret_key'] = "My-Secret-String"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['LOG_REQUEST_ID_LOG_ALL_REQUESTS'] = True
app.config['LOG_REQUEST_ID_GENERATE_IF_NOT_FOUND'] = True
RequestID(app)
initialize_logging()


swagger_url = '/swagger'
api_url = '/static/swagger.json'
swagger_blueprint = get_swaggerui_blueprint(
    swagger_url,
    api_url,
    config={
        'app_name': 'Workbench Application'
    }
)
app.register_blueprint(swagger_blueprint, url_prefix=swagger_url)
api = Api(app)


@app.before_first_request
def create_db():
    db.create_all()


@app.after_request
def append_request_id(response):
    response.headers.add('X-REQUEST-ID', current_request_id())
    return response


api.add_resource(UserResource, '/user/<string:userId>')
api.add_resource(UsersResource, '/users')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)