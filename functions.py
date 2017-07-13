from flask_sqlalchemy import SQLAlchemy
from app import db, app
from models import Blog, User

def get_blogs(userid = None):
    if userid is None:
        return Blog.query.join(User).add_columns(Blog.blog_id, Blog.blogtitle, Blog.body, Blog.imagepath, Blog.user_id, User.username).order_by(Blog.blog_id.desc()).all()
        
    else:
        return Blog.query.join(User).add_columns(Blog.blog_id, Blog.blogtitle, Blog.body, Blog.imagepath, Blog.user_id, User.username).filter_by(user_id = userid).all()

def get_users():
    return User.query.all()

def get_singleblog(blogid):
    return Blog.query.filter_by(blog_id = blogid)


def lengthnotvalid(string):
    if len(string) < 3 or len(string) > 20:
        return True
    else:
        return False

def doesnotexist(string):
    if not string or string.strip() == "":
        return True
    else:
        return False

def emailnotvalid(string):
    print(string.count('@'))
    print(string.count('.'))
    if string.count('@') == 1 and string.count('.') == 1:
        return False
    else:
        return True
def convertstrtoblank(string):
    if string is None:
        return ''
    else:
        return string