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

# SQLAlchemy engine to create the tables
Base.metadata.create_all(engine)
