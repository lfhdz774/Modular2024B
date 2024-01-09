from flask import Blueprint
from flask_restful import Api

from .resources import User, AllUsersResource

user_blueprint = Blueprint('user', __name__, url_prefix='/api/admin')
api = Api(user_blueprint)

api.add_resource(User, '/user/<string:username>')
api.add_resource(AllUsersResource, '/users')