# setup the views for the blog

# first import the render_template method
from flask import render_template

# import the other modules of the app
from blog import app
from .database import session
from .models import Post

# define the first view:
@app.route("/")
def posts():
    # use SQLAlchemy to obtain all the posts
    posts = session.query(Post)
    # order the posts by date
    posts = posts.order_by(Post.datetime.desc())
    # then return all the posts
    posts = posts.all()
    # and render them in the posts.html template
    return render_template("posts.html",
                           posts=posts
    )

