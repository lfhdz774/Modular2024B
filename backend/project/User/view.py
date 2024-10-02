from flask import Blueprint
from flask_restful import Api

from .resources import User, AllUsersResource, GetUserRoles, GetUserPositionsList, GetUserByCode, GetUsersByRole

user_blueprint = Blueprint('user', __name__, url_prefix='/api')
api = Api(user_blueprint)

api.add_resource(User, '/user')
api.add_resource(AllUsersResource, '/users')
api.add_resource(GetUserRoles, '/user/roles')
api.add_resource(GetUserPositionsList, '/user/positions')
api.add_resource(GetUserByCode, '/user/<string:code>')
api.add_resource(GetUsersByRole, '/user/role/<string:role>')