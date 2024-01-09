from flask import Blueprint
from flask_restful import Api
from .resources import Login

login_blueprint = Blueprint('login', __name__, url_prefix='/api')

api = Api(login_blueprint)

api.add_resource(Login, '/login')
