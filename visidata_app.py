#!/usr/bin/env python3

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import visidata

from create_db import Contact, Base

#MUST RUN THIS LINE IN COMMANDLINE BEFORE CALLING THIS FILE
#export PYTHONPATH=~/Desktop/visidata/


#Set Up Session
engine = create_engine('sqlite:///addressbook.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def main():
	super_secret_password = input('Password: ')
	vs = AddressBookSheet()
	visidata.run([vs])

class AddressBookSheet(visidata.SqliteSheet):
	def __init__(self):
		super().__init__("addressbook", visidata.Path("addressbook.db"), "contact")
		self.command("A", "add_entry(input('name: '), input('p_number: '))", "Add a new entry")
		self.command("d", "delete_entry(cursorRow[0])", "Delete Current Entry")
		self.command('e', 'edit_field()', 'edit this cell')
		
	def add_entry(self, name, p_number):
		newcontact = Contact(name, p_number)
		session.add(newcontact)
		session.commit()
		self.reload()
		
	def delete_entry(self, id):
		session.query(Contact).filter_by(id=id).delete()
		session.commit()
		self.reload()
		
	def edit_field(self):
		row_id = self.cursorRow[0]		
		new_val = self.editCell(self.cursorVisibleColIndex)
		field = self.cursorCol.name
		edit_field_attr = getattr(Contact, field)
		visidata.status(row_id)
		session.query(Contact).filter_by(id = row_id).update({edit_field_attr: new_val})
		session.commit()
		self.reload()

if __name__=='__main__':
	main()
