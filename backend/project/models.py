from project import db

class User(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def json(self):
        return {'id': self.id,
                'username' : self.username}

    def __repr__(self):
        return f"{self.id}. Username {self.username}"