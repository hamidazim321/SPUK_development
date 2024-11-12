from DB.Database import Database
from helpers import hash_password, verify_password


class User(Database):
    # Schema(
    # username TEXT PRIMARY KEY UNIQUE NOT NULL,
    # password_digest TEXT NOT NULL
    # )
    def __init__(self, username: str, password: str):
        super().__init__()
        self.username = username
        self.password = password

    def login_user(self) -> dict:
        """Retrieve a user based on username and verify the password."""
        try:
            self.cursor.execute(
                "SELECT username, password_digest FROM users WHERE username = ?",
                (self.username,)
            )
            user = self.cursor.fetchone()

            if user:
                password_digest = user[1]

                if verify_password(password_digest, self.password):
                    Database.set_logged_in_user(self)
                    return {"successful": True, "username": user[0]}
                else:
                    return {"successful": False, "message": "Incorrect password or username"}
            else:
                return {"successful": False, "message": "User not found"}

        except Exception as e:
            print(f"Error fetching user: {e}")
            return {"successful": False, "message": str(e)}

    def create_user(self) -> dict:
        """Add a new user to the database."""
        try:
            hashed_password = hash_password(self.password)
            self.cursor.execute(
                'INSERT INTO users (username, password_digest) VALUES (?, ?)',
                (self.username, hashed_password)
            )
            self.commit()
            self.login_user()
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
        """Delete a user based on username."""
        if self.get_logged_in_user():
            try:
                self.cursor.execute(
                    "DELETE FROM users WHERE username = ?",
                    (self.username,)
                )
                self.commit()
                Database.remove_logged_in_user()

                return {
                    "successful": True,
                    "message": f"User '{self.username}' deleted successfully."
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
        """Log out the current user."""
        Database.remove_logged_in_user()
