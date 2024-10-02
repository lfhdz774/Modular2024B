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
    


    access = db.relationship('Access', back_populates='user',foreign_keys='Access.user_id')
    notifications = db.relationship('Notification', back_populates='user')
    

    def __init__(self,username,password,email,first_name,last_name,employee_code,role_id, position_id):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.employee_code = employee_code
        self.role_id = role_id
        self.employee_position = position_id

    def json(self):
        return {'user_id': self.user_id,
                'username' : self.username,
                'email' : self.email,
                'first_name' : self.first_name,
                'last_name' : self.last_name,
                'employee_code' : self.employee_code,
                'role_id' : self.role_id,
                'employee_position' : self.employee_position
                }

    def __repr__(self):
        return f"{self.user_id}. Username {self.username}"
    
class Position(db.Model):
    __tablename__ = 'positions'

    position_id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    def json(self):
        return {
            'position_Id': self.position_id,
            'position_name': self.position_name,
            'description': self.description
        }

class Server(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'servers'

    server_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    hostname = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    pkey = db.Column(db.Text, nullable=False)
    operating_system = db.Column(db.String(50))

    access = db.relationship('Access', back_populates='server',foreign_keys='Access.server_id')
    groups = db.relationship('Group', back_populates='server', foreign_keys='Group.server_id')

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
    server_id = db.Column(db.Integer, db.ForeignKey('servers.server_id'), nullable=False)

    
    server = db.relationship('Server', back_populates='groups')

    
    def __init__(self,group_name,description,server_id):
        self.group_name = group_name
        self.description = description
        self.server_id = server_id
    def json(self):
        return{'group_name': self.group_name,
                'description' : self.description,
                'server_id' : self.server_id,
        }

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
    created_at = db.Column(db.Date)
    expires_at = db.Column(db.Date)
    user_groups = db.Column(db.ARRAY(db.Integer))
    status = db.Column(db.BOOLEAN, default=True)

    user = db.relationship('UserModel', back_populates='access')
    server = db.relationship('Server', back_populates='access')
    def __init__(self,access_name,user_id,server_id,created_at,expires_at,user_groups):
        self.access_name = access_name
        self.user_id = user_id
        self.server_id = server_id
        self.created_at = created_at
        self.expires_at = expires_at
        self.user_groups = user_groups

    def json(self):
        return {'access_id': self.access_id,
                'access_name' : self.access_name,
                'server_id' : self.server_id,
                'created_at' : str(self.created_at),
                'expires_at' : str(self.expires_at),
                'user_groups' : self.user_groups,
                }
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


class AccessRequestModel(db.Model):
    __tablename__ = 'access_requests'

    request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.server_id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    status = db.Column(db.String(20), nullable=False)
    approver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    access_id = db.Column(db.Integer, db.ForeignKey('access.access_id'), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=True)


    def __init__(self,user_id,server_id, approver_id ,access_id,requester_id, group_id):
        self.user_id = user_id
        self.server_id = server_id
        self.status = 'Pending'
        self.approver_id = approver_id
        self.access_id = access_id
        self.requester_id = requester_id
        self.group_id = group_id

         # Definición de las relaciones
    user = db.relationship('UserModel', foreign_keys=[user_id])
    server = db.relationship('Server', foreign_keys=[server_id])
    requester = db.relationship('UserModel', foreign_keys=[requester_id])
    approver = db.relationship('UserModel', foreign_keys=[approver_id])
    group = db.relationship('Group', foreign_keys=[group_id])

    def json(self):
        return {
            'request_id': self.request_id,
            'user_id': self.user_id,
            'server_id': self.server_id,
            'server_name': self.server.name if self.server else None,
            'requester_id': self.requester_id,
            'requester_name': f"{self.requester.first_name} {self.requester.last_name}" if self.requester else None, 
            'created_at': str(self.created_at),
            'status': self.status,
            'approver_id': self.approver_id,
            'access_id': self.access_id,
            'group_id': self.group_id,
            'position': self.user.Position.position_name if self.user else None,
            'role': self.user.Role.name if self.user else None,
            'group_name': self.group.group_name if self.group else None,
            'status': self.status
        }

UserModel.role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False) 
UserModel.requester_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True) # 
UserModel.approver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True) # 
UserModel.employee_position = db.Column(db.Integer, db.ForeignKey('positions.position_id'), nullable=False) #
UserModel.Position = db.relationship('Position', foreign_keys=[UserModel.employee_position])
UserModel.Role = db.relationship('Role', foreign_keys=[UserModel.role_id])
#Group.server_id = db.Column(db.Integer, db.ForeignKey('servers.server_id'), nullable=False)
UserModel.commands = db.relationship('CommandModel', back_populates='user', foreign_keys='CommandModel.user_id')