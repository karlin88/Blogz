from flask_sqlalchemy import SQLAlchemy
from app import db

class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key = True)
    blogtitle = db.Column(db.String(120))
    body = db.Column(db.Text)
    imagepath = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __init__(self, blogtitle, body, imagepath, blogger):
        self.blogtitle = blogtitle
        self.body = body
        self.imagepath = imagepath
        self.blogger = blogger

    def __repr__(self):
        return '<Blog %r>' % self.blogtitle

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.string(20))
    password = db.Column(db.string(50))
    blogs = db.relationship('Blog', backref = 'blogger')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        