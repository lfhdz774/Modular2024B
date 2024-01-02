from project import db

class User(db.Model):
    __tablename__='users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    employee_code = db.Column(db.String(20))
    role_in_application = db.Column(db.String(50))

    accesses = db.relationship('Access', back_populates='user',foreign_keys='Access.user_id')
    notifications = db.relationship('Notification', back_populates='user')

    def __init__(self,username,password,email,first_name,last_name,employee_code,role_in_application):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.employee_code = employee_code
        self.role_in_application = role_in_application

    def json(self):
        return {'user_id': self.user_id,
                'username' : self.username}

    def __repr__(self):
        return f"{self.user_id}. Username {self.username}"
    
class Group(db.Model):
    tablename = 'groups'

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    #users = db.relationship('User', secondary='users_groups_server', back_populates='groups')

    server_id = db.Column(db.Integer, db.ForeignKey('server.server_id'), nullable=False)

class Server(db.Model):
    tablename = 'servers'

    server_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_groups = db.Column(db.ARRAY(db.Integer))
    operating_system = db.Column(db.String(50))

    accesses = db.relationship('Access', back_populates='server',foreign_keys='Access.server_id')
    
class Access(db.Model):
    tablename = 'access'

    access_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    server_id = db.Column(db.Integer, db.ForeignKey('server.server_id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    expires_at = db.Column(db.TIMESTAMP)

    user_groups = db.Column(db.ARRAY(db.Integer))
    user = db.relationship('User', back_populates='accesses')
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
    user = db.relationship('User', back_populates='notifications')