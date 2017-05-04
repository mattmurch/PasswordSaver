import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Contact, Base

#Set Up Session
engine = create_engine('sqlite:///addressbook.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#NOTE: ALL FUNCTIONS TO MODIFY DB ONLY WORK WITH CONTACTS TABLE

#Working: Inserts New Contact into Database. Requires name AND p_number
def add_new_contact(name, p_number):
	newcontact = Contact(name, p_number)
	session.add(newcontact)
	session.commit()

#Working: Deletes all entries with given name
def delete_contact_by_name(name):
	session.query(Contact).filter_by(name=name).delete()
	session.commit()

#Working: Deletes all Entries with Field value == value
def delete_contact_by_field_and_value(field, value):
	field_attr = getattr(Contact, field)
	session.query(Contact).filter(field_attr == value).delete()
	session.commit()
	
#Working: Given a search field and value, edits the given field to the given value
def update_contact(search_field, search_value, edit_field, edit_value):
	search_field_attr = getattr(Contact, search_field)
	edit_field_attr = getattr(Contact, edit_field)
	session.query(Contact).filter(search_field_attr == search_value).update({edit_field_attr: edit_value})
	session.commit()
	
#Working: Replaces the field with the value of all entries with the given name
def update_contact_searched_by_name(name, field, value):
	field_attr = getattr(Contact, field)
	session.query(Contact).filter(Contact.name == name).update({field_attr: value})
	session.commit()

#Working: Prints All Entries
def print_search_all():
	contacts = session.query(Contact).all()
	for contact in contacts:
		print contact
		
#Working: Returns list of all info on all contacts
def search_all_repr():
	contactlist = []
	contacts = session.query(Contact).all()
	for contact in contacts:
		contactlist.append(contact)
	return contactlist
	
def search_all():
	contacts = session.query(Contact).all()
	return contacts
	
#Working: Returns list of all names in contact
def search_all_names():
	namelist = []
	contacts = session.query(Contact).all()
	for contact in contacts:
		namelist.append(contact.name)
	return namelist
	
#Working: Returns list of all p_numbers in contact
def search_all_p_numbers():
	p_numberlist = []
	contacts = session.query(Contact).all()
	for contact in contacts:
		p_numberlist.append(contact.p_number)
	return p_numberlist

#Working: Prints all entries with given name
def print_search_by_name(name):
	contacts = session.query(Contact).filter_by(name=name).all()
	for contact in contacts:
		print contact

#Testing Functions

#~ add_new_contact('Or', '555-555-5555')
#~ delete_contact_by_name('Matt')
#~ delete_contact_by_field_and_value('name', 'Matt')
#~ search_by_name('Or')
#~ update_contact_searched_by_name('Matt', 'p_number', '111-222-3333')
#~ update_contact('name', 'Or', 'p_number', 'Cool!')
#~ print search_all_p_numbers()
#~ print search_all()
#~ delete_contact_by_field_and_value('id', 1)
#~ print search_all()





#______________________________________________________________________________________________
#GRAVEYARD CODE FOR CONNECTION WITH POPULATE_DB FILE
#______________________________________________________________________________________________

#from populate_db import session, DBHandler

#~ x = session.query(Contact).all()
#~ print "Before Delete: ", x
#~ for y in x:
	#~ session.delete(y)
	#~ session.commit()
#~ x = session.query(Contact).all()
#~ print "After Delete: ", x

#~ example1 = Contact('Bob', '12345')
#~ DBHandler.add_contact(example1)
#~ 
#~ x = session.query(Contact).all()
#~ for y in x:
	#~ print y
#~ 
#~ DBHandler.update_contact(example1, example1.name, 'Draco')
#~ 
#~ x = session.query(Contact).all()
#~ for y in x:
	#~ print y
	
#~ x = session.query(Contact).all()
#~ for y in x:
	#~ User.delete_contact(y)
