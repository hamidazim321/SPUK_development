from DB.Database import Database
import datetime


class StudySession(Database):
    # Schema(
    # id INTEGER PRIMARY KEY AUTOINCREMENT,
    # start_time DATETIME NOT NULL,
    # end_time DATETIME NOT NULL,
    # duration_mins INTEGER NOT NULL,
    # username TEXT NOT NULL,
    # subject_name TEXT NOT NULL,
    # FOREIGN KEY(username) REFERENCES users(username),
    # FOREIGN KEY(username, subject_name) REFERENCES user_subjects(username, subject_name)
    # )

    def __init__(self, start_time=None, end_time=None):
        super().__init__()
        self.current_user = self.get_logged_in_user()
        self.start_time = start_time
        self.end_time = end_time
        self.duration_mins = None

    def start_session(self):
        """Set start_time to the current timestamp."""
        self.start_time = datetime.datetime.now()
        print(f"Session started at {self.start_time}")

    def end_session(self):
        """Set end_time to the current timestamp."""
        self.end_time = datetime.datetime.now()
        print(f"Session ended at {self.end_time}")
        self.duration_mins = (self.end_time - self.start_time).seconds // 60

    def add_session(self, subject_name: str):
        """Add session details if start and end time are provided."""
        if self.current_user:
            if self.start_time and self.end_time:
                try:
                    # Insert session details into study_sessions
                    self.cursor.execute(
                        '''
                        INSERT INTO study_sessions (username, subject_name, start_time, end_time, duration_mins) 
                        VALUES (?, ?, ?, ?, ?)
                        ''',
                        (self.current_user.username, subject_name,
                         self.start_time, self.end_time, self.duration_mins)
                    )
                    session_id = self.cursor.lastrowid

                    # Update total studied time for the subject
                    self.cursor.execute(
                        '''
                        UPDATE user_subjects 
                        SET studied_mins = studied_mins + ? 
                        WHERE username = ? AND subject_name = ?
                        ''',
                        (self.duration_mins, self.current_user.username, subject_name)
                    )

                    self.commit()
                    session_added = {
                        "successful": True,
                        "session": {
                            "id": session_id,
                            "subject_name": subject_name,
                            "start_time": self.start_time,
                            "end_time": self.end_time,
                            "duration_mins": self.duration_mins
                        }
                    }
                    self.reset_session()
                    return session_added
                except Exception as e:
                    print("Exception adding session:", str(e))
                    return {"successful": False, "message": str(e)}
            else:
                print("Start and end time must be provided")
                return {"successful": False, "message": "Start and end time must be provided"}
        else:
            print("User not found")
            return {"successful": False, "message": "User not found"}

    def reset_session(self):
        """Reset session details."""
        print("Session reset")
        self.start_time = None
        self.end_time = None
        self.duration_mins = None
