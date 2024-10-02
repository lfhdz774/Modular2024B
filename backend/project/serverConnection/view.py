from flask import Blueprint
from flask_restful import Resource
from project.models import UserModel
from flask_restful import Api,Resource

from project import app
from .resources import CreateAccess,DeleteAccess,TestConnection,GetAccess,GetAllAccesses,AddGroupToAccess
from .resources import CreateAccess,DeleteAccess,TestConnection,GetAccess, AccessRequest, GetAllRequests, ApproveRequest

serverConnection_blueprint = Blueprint('serverConnection', __name__, url_prefix='/api/admin')
api = Api(serverConnection_blueprint)

api.add_resource(CreateAccess, '/CreateAccess')
api.add_resource(DeleteAccess, '/DeleteAccess')
api.add_resource(TestConnection, '/TestConnection')
api.add_resource(GetAccess,'/GetAccess')
api.add_resource(GetAllAccesses,'/GetAllAccesses')
api.add_resource(AccessRequest,'/AccessRequest')
api.add_resource(GetAllRequests,'/GetAllRequests')
api.add_resource(ApproveRequest, '/ApproveRequest/<int:request_id>')
api.add_resource(AddGroupToAccess,'/AddGroupToAccess')


