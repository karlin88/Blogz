from flask_sqlalchemy import SQLAlchemy
from hashutils import make_pw_hash
from app import db

class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key = True)
    blogtitle = db.Column(db.String(120))
    body = db.Column(db.Text)
    imagepath = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __init__(self, blogtitle, body, blogger):
        self.blogtitle = blogtitle
        self.body = body
        self.blogger = blogger

    def __repr__(self):
        return '<Blog %r>' % self.blogtitle


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True)
    password = db.Column(db.String(500))
    blogs = db.relationship('Blog', backref = 'blogger')

    def __init__(self, username, password):
        self.username = username
        self.password = make_pw_hash(password)
