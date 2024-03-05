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
                'username' : self.username}

    def __repr__(self):
        return f"{self.user_id}. Username {self.username}"

class Server(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'servers'

    server_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_groups = db.Column(db.ARRAY(db.Integer))
    operating_system = db.Column(db.String(50))

    def __init__(self,name,ip_address,port,username,password,operating_system):
        self.name = name
        self.ip_address = ip_address
        self.port = port
        self.username = username
        self.password = password
        self.operating_system = operating_system


class Group(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'groups'

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    
    def __init__(self,group_name,description,server_id):
        self.group_name = group_name
        self.description = description
        self.server_id = server_id


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


UserModel.role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False) 
# UserModel.requester_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True) # 
# UserModel.approver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True) # 

Group.server_id = db.Column(db.Integer, db.ForeignKey('servers.server_id'), nullable=False)
