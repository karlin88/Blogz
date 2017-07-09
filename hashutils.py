import bcrypt


def make_pw_hash(password, salt=None):
    if not salt:
        salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)


def check_pw_hash(password, hash_pw):
    if bcrypt.checkpw(password, hash_pw):
        return True
    
    return False

