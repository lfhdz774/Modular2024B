from flask import Blueprint
from flask_restful import Api

from .resources import User, AllUsersResource, GetUserRoles

user_blueprint = Blueprint('user', __name__, url_prefix='/api')
api = Api(user_blueprint)

api.add_resource(User, '/user')
api.add_resource(AllUsersResource, '/users')
api.add_resource(GetUserRoles, '/user/roles')