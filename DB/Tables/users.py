from connectDB import connection
from cryptography.fernet import Fernet

cursor = connection.cursor()

def encryptPassword(password):
  with open("secret.key", "rb") as key_file:
        key = key_file.read()
  
  cipher = Fernet(key)
  return cipher.encrypt(password.encode())


def createUser(username, password):
    global cursor
    with open("secret.key", "rb") as key_file:
        key = key_file.read()
  
    cipher = Fernet(key)
    encrypted_password = encryptPassword(password)

    try:
        cursor.execute(
            'INSERT INTO users (username, password_digest) VALUES (%s, %s)', 
            (username, encrypted_password)
        )
        connection.commit()  
        return {
            successful: True,
            message: None
        }
    except Exception as e:  
        print(f"Error occurred: {e}")  
        return {
            successful: False,
            message: str(e) 
        }

# def editUser(username, password):

