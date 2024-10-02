from flask import Blueprint
from flask_restful import Resource
from project.models import UserModel
from flask_restful import Api,Resource

from project import app
from .resources import CreateGroup,DeleteGroup,TestConnection,GetGroup,GetAllGroups

serverConnection_blueprint = Blueprint('serverConnection', __name__, url_prefix='/api/admin')
api = Api(serverConnection_blueprint)

api.add_resource(CreateGroup, '/CreateGroup')
api.add_resource(DeleteGroup, '/DeleteGroup')
api.add_resource(GetGroup,'/GetGroup')
api.add_resource(GetAllGroups,'/GetAllGroups')
