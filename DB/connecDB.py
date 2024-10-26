import psycopg2
from Encrypt import Encrypt 

class Database:
    def __init__(self):
        try:
            encryptor = Encrypt()

            with open("encrypted_password.bin", "rb") as encrypted_file:
                encrypted_password = encrypted_file.read()
                
            decrypted_password = encryptor.decrypt(encrypted_password) 


            self.connection = psycopg2.connect(
                host="localhost",
                dbname="spuk",
                user="postgres",
                password=decrypted_password
            )
            self.cursor = self.connection.cursor() 
            
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self.connection = None  

    def commit(self):
        """Commit the current transaction."""
        if self.connection:
            try:
                self.connection.commit() 
                print("Transaction committed successfully.")
            except Exception as e:
                print(f"Error committing transaction: {e}")

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.cursor.close()  
            self.connection.close() 
            print("Database connection closed.")
