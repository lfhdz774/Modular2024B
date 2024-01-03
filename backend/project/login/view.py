from flask import Blueprint
from flask_restful import Resource
from flask_restful import Api,Resource

from project import app
from resources import Signup,AllUsersResource,getUser, Login, User
api = Api(app)

login_blueprint = Blueprint('login',__name__,
                                    template_folder='templates/login')

api.add_resource(Signup, '/signup') #TODO: SIGN IN RETURNING TOKEN 
api.add_resource(User, '/user')
api.add_resource(Login, '/login')
api.add_resource(getUser, '/findUser')
api.add_resource(AllUsersResource, '/allUsers')
