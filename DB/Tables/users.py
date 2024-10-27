from DB.connectDB import Database
from helpers import hash_password, verify_password

class User(Database):
    def __init__(self, name: str, password: str):
        super().__init__() 
        self.name = name
        self.password = password

    def get_user(self) -> dict:
        """Retrieve a user based on username and verify the password."""
        try:
            # Fetch user by username
            self.cursor.execute(
                "SELECT user_id, username, password_digest FROM users WHERE username = %s",
                (self.name,)
            )
            user = self.cursor.fetchone()
            
            if user:
                password_digest = bytes(user[2]) if isinstance(user[2], memoryview) else user[2]
                
                if verify_password(password_digest, self.password):
                    return {"successful": True, "user_id": user[0], "username": user[1]}
                else:
                    return {"successful": False, "message": "incorrect password or username"}

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
            return {
                "successful": True,
                "message": None
            }
        except Exception as e:
            print('Error creating user:', e)
            return {
                "successful": False,
                "message": str(e)  
            }
    
    def delete_user(self) -> dict:
        """Delete a user based on username and password."""
        user_check = self.get_user()  
        
        if user_check.get("successful"):
            try:
                self.cursor.execute(
                    "DELETE FROM users WHERE user_id = %s", 
                    (user_check["user_id"],)
                )
                self.commit()

                return {
                    "successful": True,
                    "message": f"User '{self.name}' deleted successfully."
                }

            except Exception as e:
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
