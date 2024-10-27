import bcrypt

def hash_password(password:str):
  salt = bcrypt.gensalt()
  hashed = bcrypt.hashpw(password.encode(), salt)
  return hashed
  
def verify_password(password_digest, user_password):
  return bcrypt.checkpw(user_password.encode(), password_digest)