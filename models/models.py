"""This module defines the structure of the tables in the database using sqlalchemy."""

from sqlalchemy import Column, Integer, String, ForeignKey, Binary, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

#Declase Base for database
Base = declarative_base()


class Passwords(Base):
    __tablename__ = 'passwords'
    id = Column(Integer, primary_key=True)
    site = Column(String(100))
    site_username = Column(String(100))
    site_password = Column(String(100))
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, site, site_username, site_password, user_id):
        self.site = site
        self.site_username = site_username
        self.site_password = site_password
        self.user_id = user_id


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_username = Column(String(100), unique=True)
    user_password = Column(String(100))
    user_salt = Column(String(100))
    passwords = relationship('Passwords', backref='user', lazy='dynamic')

    def __init__(self, user_username, user_password, user_salt):
        self.user_username = user_username
        self.user_password = user_password
        self.user_salt = user_salt
