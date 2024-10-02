from flask_restful import Resource,reqparse,request
from flask import jsonify,abort
from project.GenerateAccess.GenerateAccess import GenerateAccess
from project.models import Server,Access,AccessRequestModel,UserModel
from project import db
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, get_jwt, jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import create_access_token
from io import StringIO
import paramiko
from datetime import date
from sqlalchemy.orm import joinedload


from Exceptions.ServersExceptions import ServerNotFoundError,AccessAlreadyExists,AccessNotFound
from Exceptions.ServersExceptions import AccessAlreadyExistsError, ServerNotFoundError,AccessAlreadyExists

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
    def post(self):
        args = self.parser.parse_args()
        access_name = args['username']
        server_id = args['server_id']
        user_id = args['user_id']
        
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
        commands = [ f"sudo useradd -m {args['username']}"]
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
        #create Acces on DB side
        db.session.delete(access)
        db.session.commit()
        #Delete Access on the Server Side
        pem_key = server.pkey.replace("\\n","\n")
        pem_key = StringIO(pem_key)
        k = paramiko.RSAKey.from_private_key(pem_key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print ("connecting")
        c.connect( hostname = server.hostname, username = server.username, pkey = k )
        commands = [ f"sudo userdel -r {args['username']}"]
        for command in commands:
            print ("Executing {}".format( command ))
            stdin , stdout, stderr = c.exec_command(command)
            print (stdout.read())
        c.close()
        return {'msg': str(stderr.read().decode())}

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
        self.parser.add_argument('username', type=str, help='Missing username ', required=True)

    @jwt_required()
    def post(self):
        args = self.parser.parse_args()
        user_id = args['user_id']
        server_id = args['server_id']
        aprover_id = args['aprover_id']
        group_id = args['group_id']
        username = args['username']
        claims = get_jwt()
        requester_id = claims.get('user_id')
    
        #also create a temporal Access to use for when the acces is activated
        access = Access(username,user_id,server_id,date.today(),date.today(),[group_id])
        db.session.add(access)
        db.session.commit()
        db.session.refresh(access)
        print (access)
        access_id= access.access_id
        newRequest = AccessRequestModel(user_id,server_id,aprover_id,access_id,requester_id, group_id)
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
            requests = db.session().query(AccessRequestModel)\
                .join(Server, AccessRequestModel.server_id == Server.server_id)\
                .join(UserModel, AccessRequestModel.user_id == UserModel.user_id).all()
            print("Admin")
        else:
             requests = db.session().query(AccessRequestModel)\
                .join(Server, AccessRequestModel.server_id == Server.server_id)\
                .join(UserModel, AccessRequestModel.user_id == UserModel.user_id)\
                .filter(AccessRequestModel.approver_id == user_id).all()
             print("Not Admin")
             
        print([request.json() for request in requests])

        return[request.json() for request in requests]

class ApproveRequest(Resource):
    @jwt_required()
    def post(self,request_id):
        claims = get_jwt()
        aprover_id = claims.get('user_id')
        request = db.session().query(AccessRequestModel).filter_by(request_id=request_id).first()
        if not request:
            return {'msg': 'Request not Found'},404
        if request.approver_id != aprover_id:
            return {'msg': 'You are not the aprover of this request'},403
        request.status = 'Approved'

        access = db.session().query(Access).filter(Access.access_id==request.access_id).first()
        access.status = True

        db.session.add(access)
        db.session.commit()
        print(access.access_name)
        generate_access_instance = GenerateAccess()
        return generate_access_instance.crear_usuario(access.access_name)

        #return {'msg': 'Request Approved'},201  