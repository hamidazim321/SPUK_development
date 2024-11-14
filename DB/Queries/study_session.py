from DB.Database import Database
import datetime


class StudySession(Database):
    # Schema(
        # id INTEGER PRIMARY KEY AUTOINCREMENT,
        # start_time DATETIME NOT NULL,
        # end_time DATETIME NOT NULL,
        # duration_mins INTEGER NOT NULL,
        # user_id INTEGER NOT NULL,
        # subject_id INTEGER NOT NULL,
        # FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        # FOREIGN KEY (subject_id) REFERENCES user_subjects(id) ON DELETE CASCADE
    # )

    def __init__(self, subject_id=None, start_time=None, end_time=None, duration_mins=None):
        super().__init__()
        self.current_user = self.get_logged_in_user()
        self.subject_id = subject_id
        self.start_time = start_time
        self.end_time = end_time
        self.duration_mins = duration_mins
        self.id = None

    def start_session(self):
        """Set start_time to the current timestamp."""
        self.start_time = datetime.datetime.now()
        print(f"Session started at {self.start_time}")

    def end_session(self):
        """Set end_time to the current timestamp."""
        self.end_time = datetime.datetime.now()
        print(f"Session ended at {self.end_time}")

    def add_session(self):
        """Add session details if start and end time are provided."""
        if self.current_user:
            if self.start_time and self.end_time:
                self.duration_mins = (self.end_time - self.start_time).seconds // 60
                try:
                    # Insert session details into study_sessions
                    self.cursor.execute(
                        '''
                        INSERT INTO study_sessions (user_id, subject_id, start_time, end_time, duration_mins) 
                        VALUES (?, ?, ?, ?, ?)
                        ''',
                        (self.current_user.id, self.subject_id,
                         self.start_time, self.end_time, self.duration_mins)
                    )
                    self.id = self.cursor.lastrowid

                    # Update total studied time for the subject
                    self.cursor.execute(
                        '''
                        UPDATE user_subjects 
                        SET studied_mins = studied_mins + ? 
                        WHERE user_id = ? AND id = ?
                        ''',
                        (self.duration_mins, self.current_user.id, self.subject_id)
                    )

                    self.commit()
                    return {"successful": True}
                except Exception as e:
                    self.connection.rollback()
                    print("Exception adding session:", str(e))
                    return {"successful": False, "message": str(e)}
            else:
                print("Start and end time must be provided")
                return {"successful": False, "message": "Start and end time must be provided"}
        else:
            print("User not found")
            return {"successful": False, "message": "User not found"}
