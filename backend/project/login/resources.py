from flask_restful import Resource,reqparse
from flask import jsonify
from project.models import User
from project import db
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import create_access_token

class Signup(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
        self.parser.add_argument('password', type=str, help='Password of the user', required=True)
        self.parser.add_argument('email', type=str, help='Email of the user', required=True)
        self.parser.add_argument('first_name', type=str, help='First Name of the user', required=True)
        self.parser.add_argument('last_name', type=str, help='Last Name of the user', required=True)
        self.parser.add_argument('employee_code', type=str, help='Employee Code of the user', required=True)
        self.parser.add_argument('role_in_application', type=str, help='Role in the application of the user', required=True)

    @swag_from('project/swagger.yaml') 
    def get(self):
        args = self.parser.parse_args()
        username = args['username']
        user = db.session().query(User).filter_by(username).first()
        if user:
            return user.json()
        else:
            return {'username': 'not found'},404
    
    @swag_from('project/swagger.yaml')
    def post(self):
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        email = args['email']
        first_name = args['first_name']
        last_name = args['last_name']
        employee_code = args['employee_code']
        role_in_application = args['role_in_application']
        user = User(username,password,email,first_name,last_name,employee_code,role_in_application)
        db.session.add(user)
        db.session.commit()
        return {'msg': 'User Added'}

class DeleteUser(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id', type=str, help='Required user_id of the user', required=True)

    @swag_from('project/swagger.yaml') 
    def delete(self):
        args = self.parser.parse_args()
        user_id = args['user_id']
        user = db.session().query(User).filter_by(user_id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        return {'msg' : 'User Deleted'}
    
class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
        self.parser.add_argument('password', type=str, help='Password of the user', required=True)

    @swag_from('project/swagger.yaml') 
    def post(self):
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        user = db.session().query(User).filter_by(username=username).first()
        print(user)
        if username == "test" and password == "test":
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}
        else:
            return {'message': 'Invalid username or password'}, 401


class AllUsersResource(Resource):
    @swag_from('project/swagger.yaml') 
    def get(self):
        all_users = db.session.query(User).all()
        return[user.json() for user in all_users]
        
    
class getUser(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
    @swag_from('project/swagger.yaml') 
    def get(self):
        args = self.parser.parse_args()
        username = args['username']
        user = db.session().query(User).filter_by(username = username).first()
        if user:
            return user.json()
        else:
            return {'username': 'not found'},404