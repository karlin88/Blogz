from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:MyNewPass@localhost:8889/build-a-blog'
#'mysql+pymysql://build-a-blog:blogger@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

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

def get_blogs():
    return Blog.query.all()

'''class HashTags(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    hash_name = db.Column(db.String(120))

    def __init__(self,hash_name):
        self.hash_name = hash_name

class BlogPostHashTags(db.Model):
    hash_id = db.Column(db.Integer, db.ForeignKey('HashTags.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('Blog.id'))
    
    def __init__(self,hash_id,blog_id):
        self.hash_id = hash_id
        self.blog_id = blog_id'''


@app.route("/")
def index():
    return render_template('blog.html', blog = get_blogs())

if __name__ == "__main__":
    app.run()
