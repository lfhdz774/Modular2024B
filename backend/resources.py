from flask_restful import Resource, reqparse
from flask import jsonify, abort
import json
from project.models import UserModel
from project import db
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import create_access_token
from validate_email import validate_email

#exceptions import
from Exceptions.SignupExceptions import InvalidEmailError, UserAlreadyExistsError, UpdateUserInfoError, UserNotFoundError

class Signup(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
        self.parser.add_argument('password', type=str, help='Password of the user', required=True)
        self.parser.add_argument('email', type=str, help='Email of the user', required=True)
        self.parser.add_argument('first_name', type=str, help='First name of the user', required=True)
        self.parser.add_argument('last_name', type=str, help='Last name of the user', required=True)
        self.parser.add_argument('employee_code', type=str, help='Employee code of the user', required=True)
        self.parser.add_argument('role', type=str, help='Role of the user in the application', required=True)

    
    @swag_from('project/swagger.yaml') 
    def post(self):
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        email = args['email']
        first_name = args['first_name']
        last_name = args['last_name']
        employee_code = args['employee_code']
        role = args['role']

        #validate email
        try:
            isValidEmail = validate_email(email)
            if not isValidEmail:
                raise InvalidEmailError(email)
        except InvalidEmailError as e:
            abort(e.code, description=e.message)

        try:
            user = db.session().query(UserModel).filter_by(username=username).first()
            if user:
                raise UserAlreadyExistsError(username)
        except UserAlreadyExistsError as e:
            abort(e.code, description=e.message)

        user = UserModel(username, password, email, first_name, last_name, employee_code, role)
        db.session.add(user)
        db.session.commit()
        return {'msg': 'User Added'}
    

class User(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
        self.parser.add_argument('password', type=str, help='Password of the user', required=False)
        self.parser.add_argument('email', type=str, help='Email of the user', required=False)
        self.parser.add_argument('first_name', type=str, help='First name of the user', required=False)
        self.parser.add_argument('last_name', type=str, help='Last name of the user', required=False)
        self.parser.add_argument('employee_code', type=str, help='Employee code of the user', required=False)
        self.parser.add_argument('role', type=str, help='Role of the user in the application', required=False)

    @swag_from('project/swagger.yaml') 
    def get(self):
        args = self.parser.parse_args()
        username = args['username']
        try:
            user = db.session().query(UserModel).filter_by(username=username).first()
            if not user:
                raise UserNotFoundError(username)
        except UserNotFoundError as e:
            abort(e.code, description=e.message)
        except Exception as e:
            abort(500, description=e.message)

        if user:
            return user.json()
        else:
            return {'username': 'not found'}, 404

    @swag_from('project/swagger.yaml') 
    def put(self):
        self.parser.add_argument('updates', type=dict, help='Json object with the fields to update', required=True)
        args = self.parser.parse_args()
        username = args['username']
        updates = args['updates']

        # Find the user
        user = db.session().query(UserModel).filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404

        # Validate email if it's being updated
        if 'email' in updates:
            try:
                isValidEmail = validate_email(updates['email'])
                if not isValidEmail:
                    raise InvalidEmailError(updates['email'])
            except InvalidEmailError as e:
                abort(e.code, description=e.message)

        # Update the user
        for field, value in updates.items():
            setattr(user, field, value)

        # Commit the changes
        db.session().commit()

        return {'message': 'User updated successfully'}, 200
    

    @swag_from('project/swagger.yaml') 
    def delete(self):
        args = self.parser.parse_args()
        username = args['username']

        try:
            user = db.session().query(UserModel).filter_by(username=username).first()
            db.session.delete(user)
            db.session.commit()
            return {'msg' : 'User Deleted'}
        except Exception as e:
            abort(500, description=e.message)
        

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
        user = db.session().query(UserModel).filter_by(username=username).first()
        if username == user.username and password == user.password:
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid username or password'}, 401


class AllUsersResource(Resource):
    @swag_from('project/swagger.yaml') 
    def get(self):
        all_users = db.session.query(UserModel).all()
        return[user.json() for user in all_users]
        
    
class getUser(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
    @swag_from('project/swagger.yaml') 
    def get(self):
        args = self.parser.parse_args()
        username = args['username']
        user = db.session().query(UserModel).filter_by(username = username).first()
        if user:
            return user.json()
        else:
            return {'username': 'not found'},404