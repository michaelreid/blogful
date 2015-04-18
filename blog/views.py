# setup the views for the blog

# first import the render_template method
from flask import render_template, request, redirect, url_for, session, flash, g, Markup

# import the other modules of the app
from blog import app
from .database import session
from .models import Post

# to handle log-in
from flask.ext.login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from .models import User

# now define POST method for /post/add
import mistune


##############################################
      # # # DEFINE GLOBAL USER # # #
###############################################    

@app.before_request
def before_request():
    g.user = current_user

##############################################
     # # # DEFINE MARKDOWN FILTER # # #
###############################################    

@app.template_filter()
def markdown(text):
    return Markup(mistune.markdown(text,escape=True))

###############################################
      # # # VIEW ALL POSTS # # #
###############################################    

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=20):

    # pass user variable to template
    user = g.user
    
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
                           total_pages=total_pages,
                           user=user
    )


###############################################
      # # # VIEW SINGLE POSTS # # #
###############################################    

@app.route("/post/<int:id>")
def single_post(id):
    # user = g.user
    post = session.query(Post).get(id)
    print post
    return render_template("single_post.html",
                           post=post,
                           # user=user
    )


###############################################
      # # # ADDING POSTS # # #
###############################################    
# Define view for adding Posts, a form.
# The 'methods' argument in the decorator handles
# two actions.
# Need to secure posts by requiring login

@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    return render_template("add_post.html")


@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
        author=current_user
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))


###############################################
      # # # EDITING POSTS # # #
###############################################    
# Define view for editing Post form
# the 'methods' argument in the decorator 
# defines this as only for GET calls to this view
@app.route("/post/<id>/edit", methods=["GET"])
@login_required    
def edit_post_get(id):
    post = session.query(Post).get(id)
    return render_template("edit_post.html", post=post)


# now define POST method for /post/add to save
# the post to database
@app.route("/post/<id>/edit", methods=["POST"])
@login_required
def edit_post_post(id):
    post = session.query(Post).get(id)

    post.title = request.form["title"]

    post.content=mistune.markdown(request.form["content"])
    
    session.commit()
    return redirect(url_for("posts"))

    
###############################################
      # # # DELETING POSTS # # #
###############################################    

# define view for deleting a post - flash
# message asking user that they want to delete
# the current post
@app.route("/post/<id>/delete", methods=["GET"])
@login_required
def delete_post_get(id):
    post = session.query(Post).get(id)

    confirm = "<a href=\"/post/" + id + "/delete\" method=\"POST\" class=\"alert-link left-margin\">Confirm</a><a href=\"/post/" + id + "\" class=\"alert-link left-margin\">Cancel</a>"
    
    flash("Are you sure you want to delete this post?", category='danger')
    return render_template("single_post.html",
                           post=post,
                           confirm=confirm
    )

@app.route("/post/<id>/delete", methods=["POST"])  
@login_required    
def delete_post_post(id):
    session.query(Post).get(id).delete(synchronize_session=False)
    session.commit()
    return redirect(url_for('posts'))


###############################################
      # # # LOG-IN TO BLOG # # #
###############################################    

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect username or password', 'danger')
        return redirect(url_for('login_get'))

    login_user(user)
    return redirect(request.args.get('next') or url_for('posts'))

###############################################
      # # # LOG-OUT OF BLOG # # #
###############################################    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged Out", category='success')
    return redirect(url_for('posts'))