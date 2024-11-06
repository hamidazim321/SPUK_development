from DB.connectDB import Database
from helpers import hash_password, verify_password

class User(Database):
    def __init__(self, name: str, password: str):
        super().__init__() 
        self.name = name
        self.password = password
        self.id = None

    def get_user(self) -> dict:
        """Retrieve a user based on username and verify the password."""
        try:
            self.cursor.execute(
                "SELECT user_id, username, password_digest FROM users WHERE username = %s",
                (self.name,)
            )
            user = self.cursor.fetchone()
            
            if user:
                password_digest = bytes(user[2]) if isinstance(user[2], memoryview) else user[2]
                
                if verify_password(password_digest, self.password):
                    self.id = user[0]
                    self.set_current_user(self) 
                    return {"successful": True, "user_id": user[0], "username": user[1]}
                else:
                    return {"successful": False, "message": "incorrect password or username"}
            else:
                return {"successful": False, "message": "user not found"}

        except Exception as e:
            print(f"Error fetching user: {e}")
            return {"successful": False, "message": str(e)}

    def create_user(self) -> dict:
        """Add a new user to the database."""
        try:
            hashed_password = hash_password(self.password)
            self.cursor.execute(
                'INSERT INTO users (username, password_digest) VALUES (%s, %s)',
                (self.name, hashed_password)
            )
            self.commit()
            self.get_user()  
            return {
                "successful": True,
                "message": None
            }
        except Exception as e:
            self.connection.rollback()
            print('Error creating user:', e)
            return {
                "successful": False,
                "message": str(e)  
            }
    
    def delete_user(self) -> dict:
        """Delete a user based on username and password."""
        if self.get_current_user():
            try:
                self.cursor.execute(
                    "DELETE FROM users WHERE user_id = %s", 
                    (self.id,) 
                )
                self.commit()
                self.remove_current_user()

                return {
                    "successful": True,
                    "message": f"User '{self.name}' deleted successfully."
                }

            except Exception as e:
                self.connection.rollback()
                print("Error deleting user:", e)
                return {
                    "successful": False,
                    "message": str(e)
                }
        else:
            return {
                "successful": False,
                "message": "User not found."
            }
    
    def logout_user(self):
        self.remove_current_user()