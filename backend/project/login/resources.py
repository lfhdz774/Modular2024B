from flask_restful import Resource,reqparse
from flask import abort
from project.PasswordManagement.passwords import generar_hash_contrasena
from project.models import UserModel
from project import db
from flasgger.utils import swag_from
from flask_jwt_extended import create_access_token
from bcrypt import hashpw
from Exceptions.SignupExceptions import UserNotFoundError

class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
        self.parser.add_argument('password', type=str, help='Password of the user', required=True)

    @swag_from('project/swagger.yaml') 
    def post(self):
        try:
            args = self.parser.parse_args()
        except Exception as e:
            abort(400, description=str(e))
        username = args['username']
        password = args['password']
        try:
            user = db.session().query(UserModel).filter_by(username=username).first()
            if not user:
                raise UserNotFoundError(username)
        except UserNotFoundError as e:
            abort(e.code, description=e.message)

        if username == user.username and password == user.password:
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid username or password'}, 401