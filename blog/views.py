# setup the views for the blog

# first import the render_template method
from flask import render_template

# import the other modules of the app
from blog import app
from .database import session
from .models import Post

# define the first view:
@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
    # zero-indexed pages
    page_index = page -1
    
    # setup a counter to loop through posts
    count = session.query(Post).count()

    # start at first post and end at number of
    # posts per page
    start = page_index * paginate_by
    end = start + paginate_by

    # total pages calculation and prev/next 
    # buttons calculations
    total_pages = (count -1) / paginate_by + 1
    has_next = page_index < total_pages -1
    has_prev = page_index > 0

    # use SQLAlchemy to obtain all the posts
    posts = session.query(Post)
    # order the posts by date
    posts = posts.order_by(Post.datetime.desc())
    # then return all the post between start and end
    posts = posts[start:end]
    # and render them in the posts.html template
    return render_template("posts.html",
                           posts=posts,
                           has_next=has_next,
                           has_prev=has_prev,
                           page=page,
                           total_pages=total_pages
    )

# define view for single post
@app.route("/post/<id>")
def single_post(id):
    id = int(request.url[-1])
    post = session.query(Post.id == id)
    return render_template("single_post.html",
                           post=post
    )





# define view for viewing Post form
# the 'methods' argument in the decorator 
# defines this as only for GET calls to this view
@app.route("/post/add", methods=["GET"])
def add_post_get():
    return render_template("add_post.html")


# now define POST method for /post/add
import mistune
from flask import request, redirect, url_for

@app.route("/post/add", methods=["POST"])
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))

# define view for editing Post form
# the 'methods' argument in the decorator 
# defines this as only for GET calls to this view
@app.route("/post/<id>/edit", methods=["GET"])
def edit_post_get():
    return render_template("edit_post.html")


# now define POST method for /post/add
import mistune
from flask import request, redirect, url_for

@app.route("/post/<id>/edit", methods=["POST"])
def edit_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))
