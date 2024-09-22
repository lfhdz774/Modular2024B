from flask import Blueprint
from flask_restful import Resource
from project.models import UserModel
from flask_restful import Api,Resource

from project import app
from .resources import CreateAccess,DeleteAccess

serverConnection_blueprint = Blueprint('serverConnection', __name__, url_prefix='/api/admin')
api = Api(serverConnection_blueprint)

api.add_resource(CreateAccess, '/CreateAccess')
api.add_resource(DeleteAccess, '/DeleteAccess')

