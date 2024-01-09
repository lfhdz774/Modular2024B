from flask import Blueprint
from flask_restful import Resource
from project.models import UserModel
from flask_restful import Api,Resource

from project import app
from .resources import GetAllServers,ServerAdmin,AddServer

serverAdmin_blueprint = Blueprint('serverAdmin', __name__, url_prefix='/api/admin')
api = Api(serverAdmin_blueprint)

api.add_resource(GetAllServers, '/servers')
api.add_resource(ServerAdmin, '/servers/<string:server_id>')
api.add_resource(AddServer, '/servers')

