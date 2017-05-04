#Password Saver Models
from sqlalchemy import Column, Integer, String, ForeignKey, Binary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

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
		
	def __repr__(self):
		return "ID: %d, Site: %s, Username: %s, Password: %s" % (self.id, self.site, self.username, self.password)


class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	user_username = Column(String(100), unique=True)
	user_password = Column(String(100))
	passwords = relationship('Passwords', backref='user', lazy='dynamic')
	
	def __init__(self, user_username, user_password):
		self.user_username = user_username
		self.user_password = user_password
		
	#Should probably remove eventually
	def __repr__(self):
		return "username: %s, password: %s" % (self.user_username, self.user_password)

engine = create_engine('sqlite:///passwords.sqlite')

Base.metadata.create_all(engine)
