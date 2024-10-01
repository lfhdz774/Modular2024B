from flask_restful import Resource,reqparse,request
from flask import jsonify,abort
from project.models import Server,Access
from project import db
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import create_access_token
from io import StringIO
import paramiko
from datetime import date


from Exceptions.ServersExceptions import ServerNotFoundError,AccessAlreadyExistsError

class GetAllGroups(Resource):
    @swag_from('project/swagger.yaml') 
    def get(self):
        all_servers = db.session.query(Server).all()
        return[server.json() for server in all_servers]

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
                raise AccessAlreadyExistsError(server_id)
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
        user = db.session().query(Access).filter_by(access_name = access_name).first()

        #if user:
        #    return {'Error': 'Conflict',
        #            'Message': 'Access Already Exist'},409
        #else:
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
