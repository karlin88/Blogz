from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from app import db, app
from models import Blog, User
import cgi


def get_blogs():
    return Blog.query.order_by(blog.blog_id.desc()).all()

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
def index():
    blogpost = request.args.get("id")
    if blogpost is None:
        blogs = get_blogs()
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

    if doesnotexist(title):
        t_error = "Please fill in the title"
    
    if doesnotexist(postbody):
        b_error = "Please fill in the body"
    
    #return render_template('blog.html', blog = get_blogs())
    if doesnotexist(t_error) and doesnotexist(b_error):
        blog = Blog(title, postbody, image)
        db.session.add(blog)
        db.session.commit()
        return redirect ("/blog?id=" + str(blog.blog_id))
    else:
        return render_template('newpost.html',
            title_error = convertstrtoblank(t_error),
            body_error = convertstrtoblank(b_error)
        )


if __name__ == "__main__":
    app.run()
