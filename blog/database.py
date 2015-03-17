# Configure the database for Blogful app

# Basic template for working with SQLAlchemy
# import the sqlalchemy modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# import the app that will be working wtih
from blog import app

# set up the SQLAlchemy session variables
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
