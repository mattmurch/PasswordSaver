from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from create_db import Base, Contact

engine = create_engine('sqlite:///addressbook.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

class DBHandler(object):
	
#***************WHY DO WE NEED STATIC METHOD VS CREATING 
# INSTANCES OF THE CLASS
# WE GOT A TYPEERROR, TOO MANY ARGS GIVEN TO USER METHODS

#ANSWER = STATICMETHOD BIND THE METHOD TO THE CLASS OBJECT, RATHER THAN BINDING FOR EACH INSTANCE OF THE CLASS.
#THIS IS WHY YOU DO NOT NEED SELF. WE COULD CALL WITH SELF AND THAT WOULD CREATE A METHOD FOR EACH INSTANCE OF THE CLASS	
	
	@staticmethod
	def add_contact(contact):
		session.add(contact)
		session.commit()
		
	@staticmethod
	def delete_contact(contact):
		session.delete(contact)
		session.commit()

	@staticmethod
	def update_contact1(contact):
		session.query(Contact).filter_by(id=contact.id).delete()
		session.add(contact)
		session.commit()
		
	
	#~ @staticmethod
	#~ def update_contact2(contact, column, new_value):
		#~ getattr(contact, column) = new_value
		#~ session.commit()
		
	#~ @staticmethod
	#~ def update_name(contact, new_name):
		#~ contact.name = new_name
		#~ session.commit()
