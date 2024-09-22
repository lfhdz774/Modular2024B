from flask import Blueprint
from flask_restful import Resource
from flask_restful import Api,Resource

from project import app
from .resources import GetAllServers,GetServer,AddServer,DeleteServer,UpdateServer

servers_blueprint = Blueprint('serverAdmin', __name__, url_prefix='/api/admin')
api = Api(servers_blueprint)

api.add_resource(GetAllServers, '/GetServers')
api.add_resource(GetServer, '/Getserver/<string:server_id>')
api.add_resource(AddServer, '/CreateServer')
api.add_resource(DeleteServer, '/DeleteServer')
api.add_resource(UpdateServer, '/UpdateServer')