#!/usr/bin/env python3

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import visidata
import getpass

from create_db import Passwords, User, Base

#Look into database migration

#prevent user from manually accessing the database to delete things. Even though they cannot read passwords, they can still add and delete and edit stuff

#MUST RUN THIS LINE IN COMMANDLINE BEFORE CALLING THIS FILE
#export PYTHONPATH=~/Desktop/visidata/


#Set Up Session
engine = create_engine('sqlite:///passwords.sqlite')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def validate_user(input_un, input_pass):
	try:
		#Maybe find a better call that first here vvvv
		user = session.query(User).filter_by(user_username=input_un).first()
		hashed_password = user.user_password
		#Add Crypto Here
		if hashed_password == input_pass:
			return True
		else:
			return False
	except:
		print('Validate Failed')
		return False
	
def createuser(new_username, super_secret_new_password):
	#Might need to add if statement or try except statement if a user tries to create a username that is already taken
	#Dont forget to hash password before inserting
	new_user = User(new_username, super_secret_new_password)
	session.add(new_user)
	session.commit()
	
def main():
	print("Enter 'New' To Create New Account")
	current_user_username = input('Username: ')
	if current_user_username == 'New' or current_user_username == 'new':
		new_username = input('New Username: ')
		super_secret_new_password = getpass.getpass()
		#Probably need some crypto here too
		createuser(new_username, super_secret_new_password)
		print('You have been registered!')
		current_user_username = input('Username: ')
	super_secret_password = getpass.getpass()
	if validate_user(current_user_username, super_secret_password):
		current_user = session.query(User).filter_by(user_username=current_user_username).first()
		print('Current_user from current_user_username: ', current_user)
		print('User.id : ', current_user.id)
		vs = AddressBookSheet(current_user.id)
		visidata.run([vs])
	else:
		print('Invalid Login')
		main()


class AddressBookSheet(visidata.SqliteSheet):
	def __init__(self, current_user_id):
		super().__init__("passwords", visidata.Path("passwords.sqlite"), "passwords")
		self.current_user_id = current_user_id
		self.command("A", "add_entry(input('Site: '), input('Username: '), input('Password: '), current_user_id)", "Add A New Entry")
		self.command("d", "delete_entry(cursorRow[0])", "Delete Current Entry")
		self.command('e', 'edit_field()', 'Edit This Cell')

		
	def reload(self):
		super().reload()
		self.rows = [r for r in self.rows if r[4]==self.current_user_id]
		c1 = visidata.ColumnItem('Site', 1)
		c1.internal_field = 'site'
		c2 = visidata.ColumnItem('Username', 2)
		c2.internal_field = 'site_username'
		c3 = visidata.ColumnItem('Password', 3)
		c3.internal_field = 'site_password'
		self.columns = [c1,c2,c3]

	def add_entry(self, site, username, password, user_id):
		newentry = Passwords(site, username, password, user_id)
		session.add(newentry)
		session.commit()
		self.reload()
		
	def delete_entry(self, id):
		session.query(Passwords).filter_by(id=id).delete()
		session.commit()
		self.reload()
		
	def edit_field(self):
		row_id = self.cursorRow[0]		
		new_val = self.editCell(self.cursorVisibleColIndex)
		field = self.cursorCol.internal_field
		edit_field_attr = getattr(Passwords, field)
		visidata.status(row_id)
		session.query(Passwords).filter_by(id = row_id).update({edit_field_attr: new_val})
		session.commit()
		self.reload()

if __name__=='__main__':
	main()
