import datetime

# from SQLAlchemy module import the following objects
from sqlalchemy     import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# from SQLAlchemy database class import the following objects
from .database      import Base, engine

# adding users to the blog
from flask.ext.login import UserMixin              # UserMixin means inherits some default methods



# create the 'Posts' table with the following attributes

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)
    author_id = Column(Integer, ForeignKey('users.id'))        # each post can only have one author



# create users of the blog. only authenticated users will be allowed to add posts
    
class User(Base, UserMixin):                       # Creating the User model from Base
    __tablename__ = 'users'                        # SQL table name: 'users'

    id = Column(Integer, primary_key=True)         # primary key is user.id
    name = Column(String(128))                     # user's name
    email = Column(String(128), unique=True)       # user's email must be a unique field
    password = Column(String(128))                 # user's password
    posts = relationship('Post', backref='author') # relationship between author and posts: one to many

# SQLAlchemy engine to create the tables
Base.metadata.create_all(engine)
