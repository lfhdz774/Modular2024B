from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from flask import abort, request
from project.User.UserEnums import UserRoleEnum
from project.models import UserModel
from project import db
from flasgger.utils import swag_from
from validate_email import validate_email

#exceptions import
from Exceptions.SignupExceptions import InvalidEmailError, UserNotFoundError


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
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            claims = get_jwt()  # Get the payload from the token
            roles = claims.get('roles', [])  # Access roles
            # If the user is not an admin, they can only view their own profile
            if UserRoleEnum.administrador.value not in roles and UserRoleEnum.superusuario.value not in roles:
                return {'message': 'You are not authorized to view this user'}, 401

            user = db.session().query(UserModel).filter_by(username=current_user).first()
            if not user:
                raise UserNotFoundError(current_user)
        except Exception as e:
            abort(500, description=str(e)) 

        try:
            user = db.session().query(UserModel).filter_by(username=current_user).first()
            if not user:
                raise UserNotFoundError(current_user)
        except UserNotFoundError as e:
            abort(e.code, description=e.message)
        except Exception as e:
            abort(500, description=str(e)) 
        user.password = None
        return user.json()

    @swag_from('project/swagger.yaml') 
    def put(self, username):
        
        if not username:
            return {'message': 'username is required'}, 400
        
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
    def delete(self, username):
        
        if not username:
            return {'message': 'username is required'}, 400
        args = self.parser.parse_args()
        username = args['username']

        try:
            user = db.session().query(UserModel).filter_by(username=username).first()
            db.session.delete(user)
            db.session.commit()
            return {'msg' : 'User Deleted'}
        except Exception as e:
            abort(500, description=e.message)
        
class GetUserRoles(Resource):
    @swag_from('project/swagger.yaml')
    @jwt_required()
    def get(self):
        try:
            #current_user = get_jwt_identity()
            claims = get_jwt()  # Get the payload from the token
            roles = claims.get('roles', [])  # Access roles

            return roles
        except Exception as e:
            abort(500, description=str(e)) 
        



class AllUsersResource(Resource):
    @swag_from('project/swagger.yaml') 
    def get(self):
        all_users = db.session.query(UserModel).all()
        return[user.json() for user in all_users]