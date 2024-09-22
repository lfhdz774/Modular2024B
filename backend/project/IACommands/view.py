from flask import Blueprint
from flask_restful import Api
from .resources import ProcesarComando

iaCommands_blueprint = Blueprint('IACommands', __name__, url_prefix='/api')

api = Api(iaCommands_blueprint)

api.add_resource(ProcesarComando, '/commands')
