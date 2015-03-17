
# Add a DevelopmentConfig class to contain the configuration variables for
# the project. 
# Set location of the database, set the debug mode to track errors, and
# set the 'secret_key' variable to secure the calls to database
# note that key is not stored in DevConfig but in os.environ variable
import os
class DevelopmentConfig(object)
    SQLALCHEMY_DATABASE_URI = "postgresql://action@localhost:5432/blogful"
    DEBUG = TRUE
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "")
