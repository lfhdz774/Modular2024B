from project import db


class UserModel(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.LargeBinary)
    email = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    employee_code = db.Column(db.String(10), nullable=False)

    accesses = db.relationship('Access', back_populates='user',foreign_keys='Access.user_id')
    notifications = db.relationship('Notification', back_populates='user')

    def __init__(self,username,password,email,first_name,last_name,employee_code,role_id):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.employee_code = employee_code
        self.role_id = role_id

    def json(self):
        return {'user_id': self.user_id,
                'username' : self.username,
                'email' : self.email,
                'first_name' : self.first_name,
                'last_name' : self.last_name,
                'employee_code' : self.employee_code,
                'role_id' : self.role_id
                }

    def __repr__(self):
        return f"{self.user_id}. Username {self.username}"
    

class Server(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'servers'

    server_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    hostname = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    pkey = db.Column(db.Text, nullable=False)
    #user_groups = db.Column(db.ARRAY(db.Integer)) #TODO: Groups will point to the server, no the server to the groups
    operating_system = db.Column(db.String(50))

    accesses = db.relationship('Access', back_populates='server',foreign_keys='Access.server_id')
    groups = db.relationship('Group', back_populates='server', cascade='all, delete-orphan')

    def __init__(self,name,hostname,ip_address,username,pkey,operating_system):
        self.name = name
        self.hostname = hostname
        self.ip_address = ip_address
        self.username = username
        self.pkey = pkey
        self.operating_system = operating_system

    def json(self):
        return {'server_id': self.server_id,
                'name' : self.name,
                'hostname' : self.hostname,
                'ip_address' : self.ip_address,
                'username' : self.username,
                'pkey' : self.pkey,
                'operating_system' : self.operating_system
                }

    def __repr__(self):
        return f"Server ID:{self.server_id}. hostname {self.hostname}"

class Group(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'groups'

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    server = db.relationship('Server', back_populates='groups')

    
    def __init__(self,group_name,description,server_id):
        self.group_name = group_name
        self.description = description
        self.server_id = server_id

    #access_id = db.Column(db.Integer, primary_key=True)
    #access_name = db.Column(db.String(10),nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    #server_id = db.Column(db.Integer, db.ForeignKey('server.server_id'), nullable=False)
    #created_at = db.Column(db.TIMESTAMP)
    #expires_at = db.Column(db.TIMESTAMP)

class UsersGroupsServer(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'users_groups_server'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), primary_key=True, nullable=False)


class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

class Access(db.Model):
    tablename = 'access'
    access_id = db.Column(db.Integer, primary_key=True)
    access_name = db.Column(db.String(20),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.server_id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    expires_at = db.Column(db.TIMESTAMP)
    user_groups = db.Column(db.ARRAY(db.Integer))

    user = db.relationship('UserModel', back_populates='accesses')
    server = db.relationship('Server', back_populates='accesses')
    #approved_by = db.Column(db.Integer,db.ForeignKey('users.user_id'))  PENDING CHECK HOW TO DISPLAY WHO APPROVED THE REQUEST AND IF IS REQUIRED A DIFERENT TABLE? 
    
class Notification(db.Model):
    tablename = 'notifications'
    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    status = db.Column(db.String(20), nullable=False)
    user_access = db.Column(db.Integer, db.ForeignKey('access.access_id'), nullable=False)

    user = db.relationship('UserModel', back_populates='notifications')

class CommandModel(db.Model):
    __tablename__ = 'commands'
    
    command_id = db.Column(db.Integer, primary_key=True)
    comando = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    user = db.relationship('UserModel', back_populates='commands')


UserModel.role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False) 
UserModel.requester_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True) # 
UserModel.approver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True) # 

Group.server_id = db.Column(db.Integer, db.ForeignKey('servers.server_id'), nullable=False)

UserModel.commands = db.relationship('CommandModel', back_populates='user', foreign_keys='CommandModel.user_id')
