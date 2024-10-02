from flask_restful import Resource,reqparse,request
from flask import jsonify,abort
from project.models import Server,Group
from project import db
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import create_access_token
from io import StringIO
import paramiko
from datetime import date


from Exceptions.ServersExceptions import ServerNotFoundError,GroupAlreadyExists

class GetAllAccesses(Resource):
    @swag_from('project/swagger.yaml') 
    def get(self):
        all_acceses = db.session.query(Access).all()
        return[access.json() for access in all_acceses]

'''class GetAccess(Resource):
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
            return {'access_id': 'not found'},404'''
class CreateGroup(Resource):
    @swag_from('project/swagger.yaml') 
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('group_name', type=str, help='Missing group_name of the Group', required=True)
        self.parser.add_argument('description', type=str, help='Missing description of the Group', required=True)
        self.parser.add_argument('server_id', type=str, help='Missing Server_id where to create the Grpup', required=True)
    def post(self):
        args = self.parser.parse_args()
        group_name = args['group_name']
        server_id = args['server_id']
        description = args['description']
        
        #Verify that the Server Exist by Server_id
        try:
            server = db.session().query(Server).filter_by(server_id=server_id).first()
            if not server:
                raise ServerNotFoundError(server_id)
        except ServerNotFoundError as e:
            abort(404, description=str(e))
        #Verify that the Access doesnt exist on this server
        if(' ' in group_name):
            return {'msg': "Invalid Group name, No spaces are allowed"},424
        try:
            group = db.session().query(Group).filter_by(group_name = group_name,server_id=server_id).first()
            if group:
                raise GroupAlreadyExists(group_name)
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