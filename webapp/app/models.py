from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author',lazy = 'dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self,password):
       self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__ (self):
        return '<Post {}>'.format(self.body)


class Resort(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64), index=True, unique=True)
    conditions = db.relationship('Conditions', backref='loc', lazy ='dynamic')

    def __repr__(self):
        return '<Resort {}>'.format(self.location)



class Conditions(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    forcastDate = db.Column(db.DateTime, index=True)
    ltemp = db.Column(db.Integer)
    htemp = db.Column(db.Integer)
    snowDay = db.Column(db.Integer)
    snowNight = db.Column(db.Integer)
    resort_id = db.Column(db.Integer,db.ForeignKey('resort.id'))

    def __repr__ (self):
        return '<Condition {}>'.format(self.resort_id)

class SnowUpdates(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    timeStamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)

    def __repr__(self):
        return '<Last Update: {}'.format(self.timeStamp)
