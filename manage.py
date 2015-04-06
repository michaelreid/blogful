# import Flask-Script from Flask to help manage the development
# of application
import os
from flask.ext.script import Manager

# import the Flask app (defined in __init__.py)
from blog import app

# create instance of Manager
manager = Manager(app)

# setup the run command for the app
# name of function 'run' corresponds with argument given to 
# script at command line, eg python manage.py run
@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)


# setup the app manager to handle the posts
from blog.models import Post
from blog.database import session

# use a Flask-Manager decorator to seed the blog
@manager.command
def seed():
    # Using some dummy text
    content = """If you could see the earth illuminated when you were in a place as dark as night, it would look to you more splendid than the moon."""
    # create 25 posts
    for i in range(25):
        post = Post(
            title="Test Post #{}".format(i),
            content=content
        )
        # add the posts to the session
        session.add(post)
    # commit the posts to the database
    session.commit()


# add a user to test the blog with
from getpass import getpass
from werkzeug.security import generate_password_hash
from blog.models import User

@manager.command
def adduser():
    name = raw_input('Name: ')
    email = raw_input('Email: ')
    if session.query(User).filter_by(email=email).first():
        print "User with that email already exits."
        return
    password = ""
    password_2 = ""
    while not (password and password_2) or password != password_2:
        password = getpass('Password: ')
        password_2 = getpass('Re-enter password: ')
    user = User(name=name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()


# setup the __main__ function to call from command line
if __name__ == "__main__":
    manager.run()
    manager.adduser()