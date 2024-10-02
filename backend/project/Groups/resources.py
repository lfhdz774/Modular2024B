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


from Exceptions.ServersExceptions import ServerNotFoundError,GroupAlreadyExists,GroupNotFound

class GetAllGroups(Resource):
    @swag_from('project/swagger.yaml') 
    def get(self):
        all_groups = db.session.query(Group).all()
        if not all_groups:
            return {'msg': 'No Groups Found'},404
        else:
            return[groups.json() for groups in all_groups]

class GetGroup(Resource):
    @swag_from('project/swagger.yaml') 
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('group_name', type=str, help='Missing Username of the Access', required=True)
        self.parser.add_argument('server_id', type=str, help='Missing Server_id where to create the Access', required=True)
    def get(self):
        args = self.parser.parse_args()
        group_name = args['group_name']
        server_id = args['server_id']
        access = db.session().query(Group).filter_by(group_name = group_name,server_id=server_id).first()
        if access:
            return access.json()
        else:
            return {'group': 'not found'},404
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
        #Verify that the Group doesnt exist on the DB
        if(' ' in group_name):
            return {'msg': "Invalid Group name, No spaces are allowed"},424
        try:
            group = db.session().query(Group).filter_by(group_name = group_name,server_id=server_id).first()
            if group:
                raise GroupAlreadyExists(group_name)
        except ServerNotFoundError as e:
            abort(404, description=str(e))
        #create Acces on DB side
        newGroup = Group(group_name,description,server_id)
        db.session.add(newGroup)
        db.session.commit()
        #Create Access on Server Side

        pem_key = server.pkey.replace("\\n","\n")
        pem_key = StringIO(pem_key)
        k = paramiko.RSAKey.from_private_key(pem_key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print ("connecting")
        c.connect( hostname = server.hostname, username = server.username, pkey = k )
        commands = [ f"sudo groupadd {args['group_name']}"]
        for command in commands:
            print ("Executing {}".format( command ))
            stdin , stdout, stderr = c.exec_command(command)
            print (stdout.read())
        c.close()
        return {'msg': str(stderr.read().decode())}

class DeleteGroup(Resource):
    @swag_from('project/swagger.yaml') 
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('group_name', type=str, help='Missing group_name of the Group', required=True)
        self.parser.add_argument('server_id', type=str, help='Missing Server_id where to delete the Group', required=True)
    def delete(self):
        args = self.parser.parse_args()
        group_name = args['group_name']
        server_id = args['server_id']
        if(' ' in group_name):
            return {'msg': "Invalid Group name, No spaces are allowed"},424
        
        server = db.session().query(Server).filter_by(server_id=server_id).first()
        try:
            server = db.session().query(Server).filter_by(server_id=server_id).first()
            if not server:
                raise ServerNotFoundError(server_id)
        except ServerNotFoundError as e:
            abort(404, description=str(e))
        try:
            group = db.session().query(Group).filter_by(group_name = group_name,server_id=server_id).first()
            if not group:
                raise GroupNotFound(group_name)
        except GroupNotFound as e:
            abort(404, description=str(e))
        #create Acces on DB side
        db.session.delete(group)
        db.session.commit()
        #Delete Access on the Server Side
        pem_key = server.pkey.replace("\\n","\n")
        pem_key = StringIO(pem_key)
        k = paramiko.RSAKey.from_private_key(pem_key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print ("connecting")
        c.connect( hostname = server.hostname, username = server.username, pkey = k )
        commands = [ f"sudo groupdel {args['group_name']}"]
        for command in commands:
            print ("Executing {}".format( command ))
            stdin , stdout, stderr = c.exec_command(command)
            print (stdout.read())
        c.close()
        return {'msg': str(stderr.read().decode())}

class UpdateGroup(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('group_name', type=str, help='Missing group_name of the Group', required=True)
        self.parser.add_argument('server_id', type=str, help='Missing Server_id where to delete the Group', required=True)
        self.parser.add_argument('updates', type=dict, help='Json object with the fields to update', required=True)
    @swag_from('project/swagger.yaml') 
    def put(self):
        args = self.parser.parse_args()
        group_name = args['group_name']
        server_id = args['server_id']
        updates = args['updates']
        server = db.session().query(Server).filter_by(server_id=server_id).first()
        try:
            server = db.session().query(Server).filter_by(server_id=server_id).first()
            if not server:
                raise ServerNotFoundError(server_id)
        except ServerNotFoundError as e:
            abort(404, description=str(e))
        try:
            group = db.session().query(Group).filter_by(group_name = group_name,server_id=server_id).first()
            if not group:
                raise GroupNotFound(group_name)
        except GroupNotFound as e:
            abort(404, description=str(e))

        if 'update_group_name' in updates:
            for field, value in updates.items():
                setattr(group, field, value)
            pem_key = server.pkey.replace("\\n","\n")
            pem_key = StringIO(pem_key)
            k = paramiko.RSAKey.from_private_key(pem_key)
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print ("connecting")
            c.connect( hostname = server.hostname, username = server.username, pkey = k )
            commands = [ f"sudo groupmod -n {args['updates']['update_group_name']} {group.group_name}"]
            for command in commands:
                print ("Executing {}".format( command ))
                stdin , stdout, stderr = c.exec_command(command)
                print (stdout.read())
            c.close()
        elif 'description' in updates:
            for field, value in updates.items():
                setattr(group, field, value)
        else:
            return {'message': 'Property not available for update'}, 405
        
        db.session().commit()
        return {'message': 'Group updated successfully'}, 200