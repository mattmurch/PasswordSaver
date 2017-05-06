#!p3_vir_env/bin/python3

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import base64
import os
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import visidata
import getpass

from models import Passwords, User, Base

#TODO: generate requirements.txt when project is finished

#Look into database migration

#prevent user from manually accessing the database to delete things. Even though they cannot read passwords, they can still add and delete and edit stuff

#MUST RUN THIS LINE IN COMMANDLINE BEFORE CALLING THIS FILE
#export PYTHONPATH=~/Desktop/visidata/


#Set Up Session
engine = create_engine('sqlite:///passwords.sqlite')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#encrypt password and store encyption in database with username and salt. Take input password and hash it and check against hashed password in database to verify user
#use password to generate key that encrypts passwords table
def hash_pw(unhashed):
	hashed = bcrypt.hashpw(unhashed.encode('UTF-8'), bcrypt.gensalt())
	return hashed
	
def verify_hash(password, hashed):
	if bcrypt.hashpw(password.encode('UTF-8'), hashed) == hashed:
		return True
	else:
		return False

def encrypt(unencrypted, password, salt):
	kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
	key = base64.urlsafe_b64encode(kdf.derive(password.encode('UTF-8')))
	f = Fernet(key)
	return f.encrypt(unencrypted.encode('UTF-8'))
	
def decrypt(undecrypted, password, salt):
	kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
	key = base64.urlsafe_b64encode(kdf.derive(password))
	f = Fernet(key)
	return f.decrypt(undecrypted.decode('UTF-8'))

def validate_user(input_un, input_pass):
	try:
		#Maybe find a better call that first here vvvv
		user = session.query(User).filter_by(user_username=input_un).first()
		hashed_password = user.user_password
		if verify_hash(input_pass, hashed_password):
			return True
		else:
			return False
	except:
		print('Validate Failed')
		return False
	
def createuser(new_username, new_password):
	#Might need to add if statement or try except statement if a user tries to create a username that is already taken
	#Dont forget to hash password before inserting
	#Is it a bad idea to encrypt the password with itself???
	salt = os.urandom(16)
	hashed_password = hash_pw(new_password)
	new_user = User(new_username, hashed_password, salt)
	session.add(new_user)
	session.commit()
	
def main():
	print("Enter 'New' To Create New Account")
	current_user_username = input('Username: ')
	if current_user_username == 'New' or current_user_username == 'new':
		new_username = input('New Username: ')
		super_secret_new_password = getpass.getpass()
		createuser(new_username, super_secret_new_password)
		print('You have been registered!')
		current_user_username = input('Username: ')
	super_secret_password = getpass.getpass()
	if validate_user(current_user_username, super_secret_password):
		current_user = session.query(User).filter_by(user_username=current_user_username).first()
		vs = AddressBookSheet(current_user.id, super_secret_password)
		visidata.run([vs])
	else:
		print('Invalid Login')
		main()


class AddressBookSheet(visidata.SqliteSheet):
	def __init__(self, current_user_id, current_user_password):
		super().__init__("passwords", visidata.Path("passwords.sqlite"), "passwords")
		self.current_user_id = current_user_id
		self.current_user_password = current_user_password
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
		user = session.query(User).filter_by(id=user_id).first()
		newentry = Passwords(site, encrypt(username, self.current_user_password, user.user_salt), encrypt(password, self.current_user_password, user.user_salt), user_id)
		session.add(newentry)
		session.commit()
		self.reload()
		
	def delete_entry(self, id):
		session.query(Passwords).filter_by(id=id).delete()
		session.commit()
		self.reload()
		
	def edit_field(self):
		user = session.query(User).filter_by(id=user_id).first()
		row_id = self.cursorRow[0]		
		new_val = self.editCell(self.cursorVisibleColIndex)
		encrypted_new_val = encrypt(new_val, self.current_user_password, user.user_salt)
		field = self.cursorCol.internal_field
		edit_field_attr = getattr(Passwords, field)
		visidata.status(row_id)
		session.query(Passwords).filter_by(id = row_id).update({edit_field_attr: encrypted_new_val})
		session.commit()
		self.reload()

if __name__=='__main__':
	main()
