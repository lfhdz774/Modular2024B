from flask import Blueprint
from flask_restful import Resource
from project.models import UserModel
from flask_restful import Api,Resource

from project import app
from .resources import GetAllGroups,GroupAdmin,AddGroup

serverAdmin_blueprint = Blueprint('serverAdmin', __name__, url_prefix='/api/admin')
api = Api(serverAdmin_blueprint)

api.add_resource(GetAllGroups, '/groups')
api.add_resource(GroupAdmin, '/groups/<string:group_id>')
api.add_resource(AddGroup, '/groups')

