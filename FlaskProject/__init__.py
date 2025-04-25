from flask_restful import Api
from flask import Flask

from PolygonERP.models.database import db
from PolygonERP.resources.UserListResource import UserListResource


def create_app(config_object="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    api = Api(app)

    # Register resources
    api.add_resource(UserListResource, '/users')  # Create and list users
    #api.add_resource(UserResource, '/users/<int:user_id>')  # View and update user
    #api.add_resource(UserLoginResource, '/login')  # Authentication

    return app
