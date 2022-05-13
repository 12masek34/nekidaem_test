import os
import datetime
from typing import Iterator

from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session, backref, sessionmaker
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()
engine = create_engine(os.getenv('POSTGRES_DNS'))
meta = MetaData(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = 'user_'
    id = Column(Integer(), primary_key=True)
    username = Column(String(128), nullable=False)

    subscribers = relationship('Subscribe')


class Subscribe(Base):
    __tablename__ = 'subscribe'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer, ForeignKey('user_.id'))
    blog_id = Column(Integer, ForeignKey('blog.id'))

    blog = relationship('Blog')


class Blog(Base):
    __tablename__ = 'blog'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer, ForeignKey('user_.id'), unique=True)

    user = relationship('User', backref=backref('blog', uselist=False))
    post = relationship('Post', cascade='all, delete-orphan', order_by='Post.created_at')


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer(), primary_key=True)
    blog_id = Column(Integer, ForeignKey('blog.id'))
    title = Column(String(100), nullable=False)
    text = Column(String(140))
    created_at = Column(DateTime(), default=datetime.datetime.now)

    blog = relationship('Blog')


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
