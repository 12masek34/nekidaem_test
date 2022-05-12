import os
import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, Text, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session, backref
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()
engine = create_engine(os.getenv('DNS'))
meta = MetaData(bind=engine)
session = Session(bind=engine)


class User(Base):
    __tablename__ = 'user_'
    id = Column(Integer(), primary_key=True)
    username = Column(String(128), nullable=False)

    subscribers = relationship('Blog')


class Blog(Base):
    __tablename__ = 'blog'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer, ForeignKey('user_.id'), unique=True)

    user = relationship('User', backref=backref('blog', uselist=False))
    post = relationship('Post', backref='blog', cascade='all, delete-orphan')


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer(), primary_key=True)
    blog_id = Column(Integer, ForeignKey('blog.id'))
    title = Column(String(100), nullable=False)
    text = Column(String(140))
    created_at = Column(DateTime(), default=datetime.datetime.now)




# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
