from flask import Flask, request, redirect, render_template, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from app import db, app
from models import Blog, User
from hashutils import make_pw_hash, check_pw_hash
from functions import get_blogs, get_users, get_singleblog, lengthnotvalid, doesnotexist, emailnotvalid, convertstrtoblank
import cgi

app.secret_key = 'y337kGcys&zP3B'

@app.before_request
def require_login():
    allowed_routes = ['login','signup','blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        passw = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_pw_hash(passw, user.password):
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('Password incorrect or user does not exist','error')
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        existing_user = User.query.filter_by(username = username).first()
        passw = request.form['password']
        verifypass = request.form['verifypass']
        error = 0
        username_error = ''
        pass_error = ''
        vpass_error = ''
        #Error check and Produce Error messages
        if lengthnotvalid(username) or doesnotexist(username):
            username_error = "Username is not valid."
            error = 1
        elif existing_user is None:
            error = 0
        else:
            username_error = "Username already exists."
            error = 1
        
        if doesnotexist(request.form['password']):
            error = 1
            pass_error = "please enter a password."
        elif lengthnotvalid(request.form['password']):
            error = 1
            pass_error = "Password is not long enough."
        elif passw != verifypass:
            error = 1
            vpass_error = "Passwords do not match."
        #register user
        if error == 0:
            new_user = User(username,passw)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            return render_template('signup.html',
                username = convertstrtoblank(username), 
                username_error = convertstrtoblank(username_error),
                pass_error = convertstrtoblank(pass_error),
                vpass_error = convertstrtoblank(vpass_error)
            )
    else:
        return render_template('signup.html')   


@app.route("/blog")
def blog():
    blogpost = request.args.get("blogid")
    userid = request.args.get("userid")

    if blogpost is None:
        blogs = get_blogs(userid)
    else:
        blogs = get_singleblog(blogpost)
    return render_template('blog.html', blog = blogs)


@app.route("/newpost", methods=['POST','GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['blogtitle']
        postbody = request.form['body']
        image = request.form['imagepath']
        t_error = ''
        b_error = ''
        user = User.query.filter_by(username=session['username']).first()

        if doesnotexist(title):
            t_error = "Please fill in the title"
        
        if doesnotexist(postbody):
            b_error = "Please fill in the body"
        
        #return render_template('blog.html', blog = get_blogs())
        if doesnotexist(t_error) and doesnotexist(b_error):
            blog = Blog(title, postbody, user.user_id, image)
            db.session.add(blog)
            db.session.commit()
            return redirect ("/blog?blogid=" + str(blog.blog_id))
        else:
            return render_template('newpost.html',
                title_error = convertstrtoblank(t_error),
                body_error = convertstrtoblank(b_error)
            )
    else:
        return render_template('newpost.html')


@app.route("/")
def index():
    users = get_users()
    return render_template('index.html', users = users)


if __name__ == "__main__":
    app.run()
