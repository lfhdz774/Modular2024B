import bcrypt
from flask_restful import Resource, reqparse
from flask import abort
from project.models import UserModel
from project import db
from flasgger.utils import swag_from
from validate_email import validate_email
#exceptions import
from Exceptions.SignupExceptions import InvalidEmailError, UserAlreadyExistsError

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
        print(args) 

        username = args['username']
        password = args['password']
        email = args['email']
        first_name = args['first_name']
        last_name = args['last_name']
        employee_code = args['employee_code']
        role = args['role']

        try:
            isValidEmail = validate_email(email)
            if not isValidEmail:
                raise InvalidEmailError(email)
        except InvalidEmailError as e:
            abort(e.code, description=e.message)

        try:
            user = db.session.query(UserModel).filter_by(username=username).first()
            if user:
                raise UserAlreadyExistsError(username)
        except UserAlreadyExistsError as e:
            abort(e.code, description=e.message)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = UserModel(username=username, password=hashed_password, email=email, 
                         first_name=first_name, last_name=last_name, 
                         employee_code=employee_code, role_id=role)
        db.session.add(user)
        db.session.commit()
        return {'msg': 'User Added'}