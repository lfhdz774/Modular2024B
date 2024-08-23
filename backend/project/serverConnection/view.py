from flask import Blueprint
from flask_restful import Resource
from project.models import User
from flask_restful import Api,Resource

from project import app
from .resources import CreateId

serverConnection_blueprint = Blueprint('serverConnection', __name__, url_prefix='/api/admin')
api = Api(serverConnection_blueprint)

api.add_resource(CreateId, '/CreateServerId')

