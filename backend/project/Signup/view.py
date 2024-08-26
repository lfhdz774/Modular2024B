from flask import Blueprint
from flask_restful import Api

from .resources import Signup

signup_blueprint = Blueprint('signup', __name__, url_prefix='/api/admin')
api = Api(signup_blueprint)

api.add_resource(Signup, '/signup')
