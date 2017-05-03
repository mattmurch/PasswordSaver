#Address Book Program
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

#This is a test

Base = declarative_base()

#Contact Model
class Contact(Base):
	__tablename__ = 'contact'
	id = Column(Integer, primary_key=True)
	name = Column(String(250))
	p_number = Column(String(100))
	#~ email = Column(String(250))
	
	def __init__(self, name, p_number):
		self.name = name
		self.p_number = p_number
		
	#~ def update_name(self, new_name):
		#~ self.name = new_name
		#~ 
	#~ def update_p_number(self, new_p_number):
		#~ self.p_number = new_p_number
		
	def __repr__(self):
		return "ID: %d, Name: %s, Phone Number: %s" % (self.id, self.name, self.p_number)

engine = create_engine('sqlite:///addressbook.db')

Base.metadata.create_all(engine)
