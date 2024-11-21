from flask_restful import Resource,reqparse,request
from flask import jsonify,abort
from project.GenerateAccess.GenerateAccess import GenerateAccess
from project.models import Server,Access,AccessRequestModel,UserModel,Group
from project import db
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, get_jwt, jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import create_access_token
from io import StringIO
import paramiko
from datetime import date
from sqlalchemy.orm import joinedload
import time
from datetime import datetime


from Exceptions.ServersExceptions import ServerNotFoundError,AccessAlreadyExists,AccessNotFound,GroupNotFound
from Exceptions.ServersExceptions import AccessAlreadyExistsError, ServerNotFoundError,AccessAlreadyExists,AccessAlreadyAdded

class GetAllAccesses(Resource):
    @swag_from('project/swagger.yaml') 
    def get(self):
        all_acceses = db.session.query(Access).all()
        return[access.json() for access in all_acceses]

class GetAccess(Resource):
    @swag_from('project/swagger.yaml') 
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Missing Username of the Access', required=True)
        self.parser.add_argument('server_id', type=str, help='Missing Server_id where to create the Access', required=True)
    def get(self):
        args = self.parser.parse_args()
        access_name = args['username']
        server_id = args['server_id']
        access = db.session().query(Access).filter_by(access_name = access_name,server_id=server_id).first()
        if access:
            return access.json()
        else:
            return {'access_id': 'not found'},404
class CreateAccess(Resource):
    @swag_from('project/swagger.yaml') 
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Missing Username of the Access', required=True)
        self.parser.add_argument('password', type=str, help='Missing Defaut Password of the Access', required=True)
        self.parser.add_argument('server_id', type=str, help='Missing Server_id where to create the Access', required=True)
        self.parser.add_argument('user_id', type=str, help='Missing user_id owner of the Access', required=True)
        self.parser.add_argument('expiration_date', type=str, help='expiration_date of the Access', required=True)
        self.parser.add_argument('group_id', type=str, help='Group_ID of the Access', required=False,default=None)
    def post(self):
        args = self.parser.parse_args()
        access_name = args['username']
        server_id = args['server_id']
        user_id = args['user_id']
        group_id = args['group_id']
        #Verify that the Server Exist by Server_id
        try:
            server = db.session().query(Server).filter_by(server_id=server_id).first()
            if not server:
                raise ServerNotFoundError(server_id)
        except ServerNotFoundError as e:
            abort(404, description=str(e))
        #Verify that the Access doesnt exist on this server
        if(' ' in access_name):
            return {'msg': "Invalid Username, No spaces are allowed"},424
        try:
            access = db.session().query(Access).filter_by(access_name = access_name,server_id=server_id).first()
            if access:
                raise AccessAlreadyExists(access_name)
        except ServerNotFoundError as e:
            abort(404, description=str(e))
        #create Acces on DB side
        created_at = date.today()
        if group_id != None:
            group = db.session().query(Group).filter_by(group_id = group_id,server_id=server_id).first()
            groups = [group_id]
        else:
            groups = []
        newAcess = Access(access_name,user_id,server_id,created_at,args['expiration_date'],groups)
        db.session.add(newAcess)
        db.session.commit()
        #Create Access on Server Side

        pem_key = server.pkey.replace("\\n","\n")
        pem_key = StringIO(pem_key)
        k = paramiko.RSAKey.from_private_key(pem_key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print ("connecting")
        c.connect( hostname = server.hostname, username = server.username, pkey = k )
        if group_id != None:
            commands = [ f"sudo useradd -m -d /home/{args['username']} -G {group.group_name} {args['username']}"]
        else:
            commands = [ f"sudo useradd -m {args['username']} -d /home/{args['username']}"]

        for command in commands:
            print ("Executing {}".format( command ))
            stdin , stdout, stder = c.exec_command(command)
            print (stdout.read())
        commands = [f"sudo passwd {args['username']}\n"]
        for command in commands:
            print ("Executing {}".format( command ))
            stdin , stdout, stderr = c.exec_command(command)
            stdin.write(args['password']+"\n")
            stdin.write(args['password']+"\n")
            print (stdout.read())
        c.close()
        return {'msg': str(stderr.read().decode())}
    def has_spaces(input_string):
        return ' ' in input_string
    
class DeleteAccess(Resource):
    @swag_from('project/swagger.yaml') 
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Missing Username of the Access', required=True)
        self.parser.add_argument('server_id', type=str, help='Missing Server_id where to Delete the Access', required=True)
    def delete(self):
        args = self.parser.parse_args()
        access_name = args['username']
        server_id = args['server_id']
        server = db.session().query(Server).filter_by(server_id=server_id).first()

        try:
            server = db.session().query(Server).filter_by(server_id=server_id).first()
            if not server:
                raise ServerNotFoundError(server_id)
        except ServerNotFoundError as e:
            abort(404, description=str(e))
        try:
            access = db.session().query(Access).filter_by(access_name = access_name,server_id=server_id).first()
            if not access:
                raise AccessNotFound(access_name)
        except ServerNotFoundError as e:
            abort(404, description=str(e))

        try:

            pem_key = server.pkey.replace("\\n","\n")
            pem_key = StringIO(pem_key)
            k = paramiko.RSAKey.from_private_key(pem_key)
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print ("connecting")
            c.connect( hostname = server.hostname, username = server.username, pkey = k )
            commands = [ f"sudo userdel -f -r {access.access_name}"]
            for command in commands:
                print ("Executing {}".format( command ))
                stdin , stdout, stderr = c.exec_command(command)
                output = stdout.read().decode().strip()
                error = stderr.read().decode().strip()

                if error:
                    print(f"Error: {error}")

                print(f"Command output: {output}")
            c.close()

            db.session.delete(access)
            db.session.commit()
            return {'msg': str(stderr.read().decode())}
        except Exception as e:
            print(e)
            return {'msg': str(e)},500

        

class AddGroupToAccess(Resource):
    @swag_from('project/swagger.yaml') 
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Missing Username of the Access', required=True)
        self.parser.add_argument('server_id', type=str, help='Missing Server_id where to Delete the Access', required=True)
        self.parser.add_argument('group_name', type=str, help='Missing group_name of the Group', required=True)
    def post(self):
        args = self.parser.parse_args()
        access_name = args['username']
        server_id = args['server_id']
        group_name = args['group_name']
        server = db.session().query(Server).filter_by(server_id=server_id).first()
        try:
            server = db.session().query(Server).filter_by(server_id=server_id).first()
            if not server:
                raise ServerNotFoundError(server_id)
        except ServerNotFoundError as e:
            abort(404, description=str(e))
        try:
            access = db.session().query(Access).filter_by(access_name = access_name,server_id=server_id).first()
            if not access:
                raise AccessNotFound(access_name)
        except ServerNotFoundError as e:
            abort(404, description=str(e))
        try:
            group = db.session().query(Group).filter_by(group_name = group_name,server_id=server_id).first()
            if not group:
                raise GroupNotFound(group_name)
        except GroupNotFound as e:
            abort(404, description=str(e))
        try:
            for i in access.user_groups:
                if i == group.group_id:
                    raise AccessAlreadyAdded(group_name)
        except AccessAlreadyAdded as e:
            abort(409, description=str(e))
        #Update Acces on DB side
        updatedUser_Groups = access.user_groups + [group.group_id]
        access.user_groups = updatedUser_Groups
        db.session().commit()

        #Update Access on Server Side

        pem_key = server.pkey.replace("\\n","\n")
        pem_key = StringIO(pem_key)
        k = paramiko.RSAKey.from_private_key(pem_key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print ("connecting")
        c.connect( hostname = server.hostname, username = server.username, pkey = k )
        commands = [ f"sudo usermod -a -G {group.group_name} {access.access_name} "]
        for command in commands:
            print ("Executing {}".format( command ))
            stdin , stdout, stder = c.exec_command(command)
            print (stdout.read())
        c.close()
        return {'msg': str(stder.read().decode())}
    

class RemoveGroupFromAccess(Resource):
    @swag_from('project/swagger.yaml') 
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Missing Username of the Access', required=True)
        self.parser.add_argument('server_id', type=str, help='Missing Server_id where to Delete the Access', required=True)
        self.parser.add_argument('group_name', type=str, help='Missing group_name of the Group', required=True)
    def post(self):
        args = self.parser.parse_args()
        access_name = args['username']
        server_id = args['server_id']
        group_name = args['group_name']
        server = db.session().query(Server).filter_by(server_id=server_id).first()
        try:
            server = db.session().query(Server).filter_by(server_id=server_id).first()
            if not server:
                raise ServerNotFoundError(server_id)
        except ServerNotFoundError as e:
            abort(404, description=str(e))
        try:
            access = db.session().query(Access).filter_by(access_name = access_name,server_id=server_id).first()
            if not access:
                raise AccessNotFound(access_name)
        except ServerNotFoundError as e:
            abort(404, description=str(e))
        try:
            group = db.session().query(Group).filter_by(group_name = group_name,server_id=server_id).first()
            if not group:
                raise GroupNotFound(group_name)
        except GroupNotFound as e:
            abort(404, description=str(e))
        #Update Acces on DB side
        access.user_groups = [num for num in access.user_groups if num != group.group_id]
        print(access.user_groups)
        db.session().commit()
        #Update Access on Server Side

        pem_key = server.pkey.replace("\\n","\n")
        pem_key = StringIO(pem_key)
        k = paramiko.RSAKey.from_private_key(pem_key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print ("connecting")
        c.connect( hostname = server.hostname, username = server.username, pkey = k )
        commands = [ f"sudo gpasswd  -d {access.access_name} {group.group_name}  "]
        for command in commands:
            print ("Executing {}".format( command ))
            stdin , stdout, stder = c.exec_command(command)
            print (stdout.read())
        c.close()
        return {'msg': str(stder.read().decode())}

class TestConnection(Resource):
    @swag_from('project/swagger.yaml') 
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('server_id', type=str, help='Missing Server_id where to test the Connection', required=True)
    def get(self):
        args = self.parser.parse_args()
        server_id = args['server_id']
        server = db.session().query(Server).filter_by(server_id=server_id).first()
        try:
            server = db.session().query(Server).filter_by(server_id=server_id).first()
            if not server:
                raise ServerNotFoundError(server_id)
        except ServerNotFoundError as e:
            abort(404, description=str(e))
        pem_key = server.pkey.replace("\\n","\n")
        pem_key = StringIO(pem_key)
        k = paramiko.RSAKey.from_private_key(pem_key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print ("connecting")
        c.connect( hostname = server.hostname, username = server.username, pkey = k )
        commands = [ f"echo $SSH_CONNECTION"]
        for command in commands:
            print ("Executing {}".format( command ))
            stdin , stdout, stderr = c.exec_command(command)
            print (stdout.read())
        
        c.close()
        if str(stdout.read().decode()) == "":
            return {'msg': "Connection Successfull"}
        else:
            return {'msg': "Connection Fail"}

class AccessRequest(Resource):
    @swag_from('project/swagger.yaml') 
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id', type=str, help='Missing user_id ', required=True)
        self.parser.add_argument('server_id', type=str, help='Missing Server_id ', required=True)
        self.parser.add_argument('aprover_id', type=str, help='Missing aprover_id ', required=True)
        self.parser.add_argument('group_id', type=str, help='Missing group_id ', required=True)

    @jwt_required()
    def post(self):
        args = self.parser.parse_args()
        user_id = args['user_id']
        server_id = args['server_id']
        aprover_id = args['aprover_id']
        group_id = args['group_id']
        claims = get_jwt()
        requester_id = claims.get('user_id')
    
        newRequest = AccessRequestModel(user_id,server_id,aprover_id,None,requester_id, group_id)
        db.session.add(newRequest)
        db.session.commit()
        return {'msg': 'Request Created'},201

class AccessRequestForMe(Resource):
    @jwt_required()
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('server_id', type=str, help='Missing Server_id ', required=True)
        self.parser.add_argument('group_id', type=str, help='Missing group_id ', required=True)
        self.parser.add_argument('approver_id', type=str, help='Missing approver_id ', required=True)


    @jwt_required()
    def post(self):
        args = self.parser.parse_args()
        server_id = args['server_id']
        group_id = args['group_id']
        approver_id = args['approver_id']
        claims = get_jwt()
        user_id = claims.get('user_id')

        newRequest = AccessRequestModel(user_id,server_id,approver_id,None,user_id, group_id)

        
        db.session.add(newRequest)
        db.session.commit()
        return {'msg': 'Request Created'},201
class GetAllRequests(Resource):   
    @jwt_required()
    def get(self):
        claims = get_jwt()
        user_id = claims.get('user_id')
        user_role = claims.get('roles')
        print(user_role)

        if 7 in user_role:
            requests = db.session().query(AccessRequestModel).add_entity(UserModel)\
                .join(Server, AccessRequestModel.server_id == Server.server_id)\
                .join(UserModel, AccessRequestModel.user_id == UserModel.user_id).filter(AccessRequestModel.status == 'Pending').all()
        else:
             requests = db.session().query(AccessRequestModel).add_entity(UserModel)\
                .join(Server, AccessRequestModel.server_id == Server.server_id)\
                .join(UserModel, AccessRequestModel.user_id == UserModel.user_id)\
                .filter(AccessRequestModel.approver_id == user_id).filter(AccessRequestModel.status == 'Pending').all()
             
        print([{'access_request': access_request.json(), 'user': user.json()} for access_request, user in requests])

        result = [{'access_request': access_request.json(), 'user': user.json()} for access_request, user in requests]
        return result

class ApproveRequest(Resource):
    @jwt_required()
    def post(self,request_id):
        claims = get_jwt()
        aprover_id = claims.get('user_id')
        request = db.session().query(AccessRequestModel).filter_by(request_id=request_id).first()
        if not request:
            return {'message': 'Request not Found'},404
        if request.approver_id != aprover_id:
            return {'message': 'You are not the aprover of this request'},403
        request.status = 'Approved'


        data = db.session.query(AccessRequestModel).filter_by(request_id=request_id)\
            .join(Server, AccessRequestModel.server_id == Server.server_id)\
            .join(UserModel, AccessRequestModel.requester_id == UserModel.user_id)\
            .with_entities(
                UserModel.employee_code,
                Server.short_name,
                UserModel.email,
                Server.hostname
                )\
            .first()
       
        generate_access_instance = GenerateAccess()

        userName = generate_access_instance.generar_username(data)

        groupArray = []
        groupArray.append(request.group_id)
        access = Access(userName,request.user_id,request.server_id, date.today(),None,groupArray)

        request.status = 'Approved'

        userCreated = generate_access_instance.crear_usuario(userName, request.server_id, data.email, request.group_id, data.hostname )

        if not userCreated['result']:
            return userCreated,500
        


        db.session.add(access)
        db.session.commit()


        return userCreated

class GetAccessByUser(Resource):
    @jwt_required()
    def post(self,user_id):

        claims = get_jwt()
        requester_id = claims.get('user_id')
        requester_user = db.session().query(UserModel).filter_by(user_id=requester_id).first()

        if not requester_user:
            return {'message': 'User not Found'},404
        
        if requester_user.role_id != 7:
            return {'message': 'Unauthorized access'},403
        
        UserAccesses = db.session().query(Access).filter_by(user_id=user_id)\
            .join(Server, Access.server_id == Server.server_id)\
            .with_entities(
                Access.access_name,
                Access.user_groups,
                Access.created_at,
                Access.status,
                Server.name,
                Server.server_id
                )\
            .all()
        
        result = [
            {
                'access_name': access.access_name,
                'user_groups': access.user_groups,
                'created_at': access.created_at.isoformat() if isinstance(access.created_at, datetime) else str(access.created_at),
                'status': access.status,
                'server_name': access.name,
                'server_id': access.server_id
            }
            for access in UserAccesses
        ]

        return result, 200
class GetAccessMyUser(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        requester_id = claims.get('user_id')
        requester_user = db.session().query(UserModel).filter_by(user_id=requester_id).first()

        if not requester_user:
            return {'message': 'User not Found'},404
        
        UserAccesses = db.session().query(Access).filter_by(user_id=requester_id)\
            .join(Server, Access.server_id == Server.server_id)\
            .with_entities(
                Access.access_name,
                Access.user_groups,
                Access.created_at,
                Access.status,
                Server.name,
                Server.server_id
                )\
            .all()
        
        result = [
            {
                'access_name': access.access_name,
                'user_groups': access.user_groups,
                'created_at': access.created_at.isoformat() if isinstance(access.created_at, datetime) else str(access.created_at),
                'status': access.status,
                'server_name': access.name,
                'server_id': access.server_id
            }
            for access in UserAccesses
        ]

        return result, 200
