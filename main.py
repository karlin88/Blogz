from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from app import db, app
from models import Blog, User
from hashutils import make_pw_hash, check_pw_hash
import cgi


def get_blogs(userid = None):
    if userid is None:
        return Blog.query.order_by(Blog.blog_id.desc()).all()
    else:
        return Blog.query.filter_by(user_id = userid).all()

def get_users():
    return User.query.all()

def get_singleblog(blogid):
    return Blog.query.filter_by(id = blogid)

def doesnotexist(string):
    if not string or string.strip() == "":
        return True
    else:
        return False

def convertstrtoblank(string):
    if string is None:
        return ''
    else:
        return string

@app.route("/blog")
def blog():
    blogpost = request.args.get("blogid")
    userid = request.args.get("userid")

    if blogpost is None:
        blogs = get_blogs(userid)
    else:
        blogs = get_singleblog(blogpost)
    return render_template('blog.html', blog = blogs)

@app.route("/newpost")
def newblogform():
    return render_template('newpost.html')


@app.route("/newpost", methods=['POST'])
def add_post():
    title = request.form['blogtitle']
    postbody = request.form['body']
    image = request.form['imagepath']
    
    user = request.args.get("user")

    if doesnotexist(title):
        t_error = "Please fill in the title"
    
    if doesnotexist(postbody):
        b_error = "Please fill in the body"
    
    #return render_template('blog.html', blog = get_blogs())
    if doesnotexist(t_error) and doesnotexist(b_error):
        blog = Blog(title, postbody, image)
        db.session.add(blog)
        db.session.commit()
        return redirect ("/blog?blogid=" + str(blog.blog_id))
    else:
        return render_template('newpost.html',
            title_error = convertstrtoblank(t_error),
            body_error = convertstrtoblank(b_error)
        )

@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if not user:
        return redirect("/login?error=userdoesntexist")
    elif check_pw_hash(request.form['password'], user.password):
        return redirect ("/singleuser?userid=" + user.user_id)
    else:
        return redirect("/login?error=" + "incorrectpassword")


@app.route("/signup", methods=['POST'])
def signup():
    username = request.form['username']
    password = make_pw_hash(request.form['password'])

    user = User(username,password)
    db.session.add(user)
    db.session.commit()

    return redirect ("/newpost")


@app.route("/")
def index():
    users = get_users()
    return render_template('index.html', users = users)


if __name__ == "__main__":
    app.run()
