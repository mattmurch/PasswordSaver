#!/usr/bin/env python3

import base64
import getpass
import os

import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
import visidata

from .models.models import Passwords, User, Base


# Build database and set up session
engine = create_engine('sqlite:///passwords.sqlite')
Base.metadata.bind = engine
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


def hash_pw(unhashed):
    """Takes a password. Returns its bcrypt hash."""
    hashed = bcrypt.hashpw(unhashed.encode('UTF-8'), bcrypt.gensalt())
    return hashed


def verify_hash(password, hashed):
    """Takes a password and a hash. Returns if the hashed password matches the hash."""
    return hashed == bcrypt.hashpw(password.encode('UTF-8'), hashed)


def generate_key(password, salt):
    """Takes a password and a salt. Returns an encryption/decryption key."""
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password.encode('UTF-8')))
    return key


def encrypt(unencrypted, key):
    """Takes a string and a key. Returns the encrypted string."""
    return Fernet(key).encrypt(unencrypted.encode('UTF-8'))


def decrypt(undecrypted, key):
    """Takes an encrypted string and the key that string was encrypted with. Returns the decrypted string."""
    return Fernet(key).decrypt(undecrypted).decode('UTF-8')


def validate_user(input_un, input_pass):
    """Takes username and password. Checks User table in database for username and
    hashed password pair. Returns True if there is a match.
    """
    try:
        user = session.query(User).filter_by(user_username=input_un).first()
        hashed_password = user.user_password
        return verify_hash(input_pass, hashed_password)
    except:
        print('Validate Failed')
        return False


def create_user():
    """Asks for username. If username already exists in the database, asks for a different
    username. If the username is original, asks for password, and creates a new entry in the
    User table with the new username, the hashed password, and a randomly generated salt.
    """
    new_username = input('New Username: ')
    if session.query(exists().where(User.user_username==new_username)).scalar():
        print('This username is already taken. Please use a different username.')
        create_user()
    elif new_username in ['New', 'new']:
        print('You cannot have that username. Pick a different one.')
        create_user()
    else:
        new_password = getpass.getpass()
        salt = os.urandom(16)
        hashed_password = hash_pw(new_password)
        new_user = User(new_username, hashed_password, salt)
        session.add(new_user)
        session.commit()


def main():
    """Asks for username and password, and calls validate_user on them.
    If validate_user returns true, opens visidata sheet for the user's information.
    If the given username is 'New' or 'new', calls create_user.
    """
    print("Enter 'New' To Create New Account")
    current_user_username = input('Username: ')
    if current_user_username in ['New', 'new']:
        create_user()
        print('You have been registered!')
        current_user_username = input('Username: ')
    current_user_password = getpass.getpass()
    if validate_user(current_user_username, current_user_password):
        current_user = session.query(User).filter_by(user_username=current_user_username).first()
        vs = PasswordSaverSheet(current_user, current_user_password)
        visidata.run([vs])
    else:
        print('Invalid Login')
        main()


class PasswordSaverSheet(visidata.SqliteSheet):
    """This class defines the sheet displayed by visidata and PasswordSaver's custom functions.
    This sheet displays the passwords table for the current user.
    """

    def __init__(self, current_user, current_user_password):
        """Initializes variables that are unique to each sheet: the user, user id, user password, and encryption key."""
        super().__init__("passwords", visidata.Path("passwords.sqlite"), "passwords")
        self.current_user = current_user
        self.current_user_id = current_user.id
        self.current_user_password = current_user_password
        self.current_key = generate_key(current_user_password, current_user.user_salt)
        self.command("A", "add_entry(input('Site: '), input('Username: '), input('Password: '), current_user_id)", "Add A New Entry")
        self.command("d", "delete_entry(cursorRow[0])", "Delete Current Entry")
        self.command('e', 'edit_field(current_user_id)', 'Edit This Cell')

    def make_decrypt(self, user, col_number):
        """Takes a user and a column number. Returns a function that decrypts the values in the given column."""
        def temp_decrypt(r, self=self, salt=self.current_user.user_salt, col_number=col_number):
            return decrypt(r[col_number], self.current_key)
        return temp_decrypt

    def reload(self):
        """Reloads the decrypted values in the passwords table that belong to the current user."""
        super().reload()
        user = self.current_user
        self.rows = [r for r in self.rows if r[4] == self.current_user.id]
        c1 = visidata.Column('Site', getter=self.make_decrypt(user, 1))
        c1.internal_field = 'site'
        c2 = visidata.Column('Username', getter=self.make_decrypt(user, 2))
        c2.internal_field = 'site_username'
        c3 = visidata.Column('Password', getter=self.make_decrypt(user, 3))
        c3.internal_field = 'site_password'
        self.columns = [c1, c2, c3]

    def add_entry(self, site, username, password, user_id):
        """Takes a site, username, password, and user_id. Adds the encrypted site, user,
        and password to the passwords table of the user.
        """
        user = self.current_user
        newentry = Passwords(encrypt(site, self.current_key), encrypt(username, self.current_key), encrypt(password, self.current_key), user_id)
        session.add(newentry)
        session.commit()
        self.reload()

    def delete_entry(self, id):
        """Deletes the currently selected row from the database."""
        session.query(Passwords).filter_by(id=id).delete()
        session.commit()
        self.reload()

    def edit_field(self, user_id):
        """Edits the currently selected value, encrypts it, and updates the database."""
        user = self.current_user
        row_id = self.cursorRow[0]
        new_val = self.editCell(self.cursorVisibleColIndex)
        encrypted_new_val = encrypt(new_val, self.current_key)
        field = self.cursorCol.internal_field
        edit_field_attr = getattr(Passwords, field)
        visidata.status(row_id)
        session.query(Passwords).filter_by(id=row_id).update({edit_field_attr: encrypted_new_val})
        session.commit()
        self.reload()


if __name__ == '__main__':
    main()
