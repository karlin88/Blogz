import hashlib
import random
import string
# from flask import Flask
# from flask.ext.bcrypt import Bcrypt
# from app import app
# bcrypt = Bcrypt(app)

# def make_pw_hash(password, salt=None):
#     if not salt:
#         salt = bcrypt.gensalt()
#     return bcrypt.hashpw(password, salt)


# def check_pw_hash(password, hash_pw):
#     if bcrypt.checkpw(password, hash_pw):
#         return True

#     return False


def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])


def make_pw_hash(password, salt=None):
    if not salt:
        salt = make_salt()
    hash = hashlib.sha256(str.encode(password + salt)).hexdigest()
    return '{hash},{salt}'.format(hash = hash, salt = salt)
    
    # hash = hashlib.sha256(str.encode(password)).hexdigest()
    # return '{0}'.format(hash)


def check_pw_hash(password, hash):
    salt = hash.split(',')[1]
    if make_pw_hash(password, salt) == hash:
        return True

    return False