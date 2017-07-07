from flask_sqlalchemy import SQLAlchemy
from app import db

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    blogtitle = db.Column(db.String(120))
    body = db.Column(db.Text)
    imagepath = db.Column(db.String(120))

    def __init__(self, blogtitle, body, imagepath):
        self.blogtitle = blogtitle
        self.body = body
        self.imagepath = imagepath

    def __repr__(self):
        return '<Blog %r>' % self.blogtitle