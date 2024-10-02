from flask import Blueprint
from flask_restful import Resource
from project.models import UserModel
from flask_restful import Api,Resource

from project import app
from .resources import CreateGroup,GetGroup,DeleteGroup,GetAllGroups,UpdateGroup
groups_blueprint = Blueprint('groups_blueprint', __name__, url_prefix='/api/admin')
api = Api(groups_blueprint)

api.add_resource(CreateGroup, '/CreateGroup')
api.add_resource(DeleteGroup, '/DeleteGroup')
api.add_resource(GetGroup,'/GetGroup')
api.add_resource(GetAllGroups,'/GetAllGroups')
api.add_resource(UpdateGroup,'/UpdateGroup')
