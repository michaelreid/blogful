####
#
# Blogful: a Flask blogging application
#
# Version 0.1
#
# March 2015
#
####

# import the Flask class from Flask module
from flask import Flask

# setup the app as an instance of the Flask object
app = Flask(__name__)

# import the views and filters from current module
from . import views  # import Jinja views
from . import filters # import Jinja filters

# both views and filters come after the app has been created as
# they make use of the object

