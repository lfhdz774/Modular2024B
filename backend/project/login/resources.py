from flask_restful import Resource,reqparse,request
from project.models import UserModel
from project import db
from flasgger.utils import swag_from
from flask_jwt_extended import create_access_token

class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
        self.parser.add_argument('password', type=str, help='Password of the user', required=True)

    @swag_from('project/swagger.yaml') 
    def get(self):
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        user = db.session().query(UserModel).filter_by(username=username).first()
        if username == user.username and password == user.password:
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid username or password'}, 401