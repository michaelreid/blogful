import datetime

# from SQLAlchemy module import the following objects
from sqlalchemy import Column, Integer, String, Text, DateTime

# from SQLAlchemy database class import the following objects
from .database import Base, engine

# create the 'Posts' table with the following attributes
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)

# adding users to the blog
from flask.ext.login import UserMixin              # UserMixin means inherits some default methods

class User(Base, UserMixin):                       # Creating the User model from Base
    __tablename__ = 'users'                        # SQL table name: 'users'

    id = Column(Integer, primary_key=True)         # primary key is user.id
    name = Column(String(128))                     # user's name
    email = Column(String(128), unique=True)       # user's email must be a unique field
    password = Column(String(128))                 # user's password

# SQLAlchemy engine to create the tables
Base.metadata.create_all(engine)
