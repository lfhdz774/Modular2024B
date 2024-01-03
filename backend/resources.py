from flask_restful import Resource,reqparse
from flask import jsonify, abort
from project.models import User
from project import db
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import create_access_token
from validate_email import validate_email
from password_strength import PasswordPolicy

#exceptions import
from Exceptions.SignupExceptions import InvalidEmailError, InvalidPasswordError, UserAlreadyExistsError

class Signup(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
        self.parser.add_argument('password', type=str, help='Password of the user', required=True)
        self.parser.add_argument('username', type=str, help='Username of the user', required=True)
        self.parser.add_argument('password', type=str, help='Password of the user', required=True)
        self.parser.add_argument('email', type=str, help='Email of the user', required=True)
        self.parser.add_argument('first_name', type=str, help='First name of the user', required=True)
        self.parser.add_argument('last_name', type=str, help='Last name of the user', required=True)
        self.parser.add_argument('employee_code', type=str, help='Employee code of the user', required=True)
        self.parser.add_argument('role', type=str, help='Role of the user in the application', required=True)

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
        self.parser.add_argument('email', type=str, help='Email of the user', required=True)
        self.parser.add_argument('first_name', type=str, help='First name of the user', required=True)
        self.parser.add_argument('last_name', type=str, help='Last name of the user', required=True)
        self.parser.add_argument('employee_code', type=str, help='Employee code of the user', required=True)
        self.parser.add_argument('role', type=str, help='Role of the user in the application', required=True)
        
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        email = args['email']
        first_name = args['first_name']
        last_name = args['last_name']
        employee_code = args['employee_code']
        role = args['role']

        #validation of email and password
        try:
            isValidEmail = validate_email(email)
            if not isValidEmail:
                raise InvalidEmailError(email)
        except InvalidEmailError as e:
            abort(e.code, description=e.message)
            
        policy = PasswordPolicy.from_names(
            length=8,  # min length: 8
            uppercase=1,  # need min. 2 uppercase letters
            numbers=1,  # need min. 2 digits
            special=1,  # need min. 2 special characters
            nonletters=1,  # need min. 2 non-letter characters (digits, specials, anything)
        )
        try:
            password_errors = policy.test(password)
            if password_errors:
                error_messages = [str(error) for error in password_errors]
                # log the errors
                if error_messages:
                    print(f"Password validation errors: {', '.join(error_messages)}")
                    raise InvalidPasswordError(password, error_messages)
        except InvalidPasswordError as e:
            abort(e.code, description=e.message)

        try:
            user = db.session().query(User).filter_by(username=username).first()
            if user:
                raise UserAlreadyExistsError(username)
        except UserAlreadyExistsError as e:
            abort(e.code, description=e.message)

        user = User(username, password, email, first_name, last_name, employee_code, role)
        db.session.add(user)
        db.session.commit()
        return {'msg': 'User Added'}

    @swag_from('project/swagger.yaml') 
    def delete(self,id):
        user = db.session().query(User).filter_by(id=id).first()
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