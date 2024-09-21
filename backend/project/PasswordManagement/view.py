from flask import Blueprint
from flask_restful import Api
from .resources import PasswordView

PasswordView_blueprint = Blueprint('firstLogin', __name__, url_prefix='/api')

api = Api(PasswordView_blueprint)

api.add_resource(PasswordView, '/first-login/password/<string:token>')
