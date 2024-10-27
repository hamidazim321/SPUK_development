from DB.Tables.users import User
from DB.Tables.subjects import Subject
import datetime

class Session:
    def __init__(self, user: User, subject: Subject, start_time=None, end_time=None):
        self.user = user
        self.subject = subject
        self.start_time = start_time
        self.end_time = end_time

    def start_session(self):
        """Set start_time to the current timestamp."""
        if self.user.get_current_user():
            self.start_time = datetime.datetime.now()
            print(f"Session started at {self.start_time}")
            return True
        else:
            print("User not found")
            return False
    
    def end_session(self):
        """Set end_time to the current timestamp."""
        if self.user.get_current_user():
            self.end_time = datetime.datetime.now()
            print(f"Session ended at {self.end_time}")
            return True
        else:
            print("User not found")
            return False

    def add_session(self):
        """Add session details if start and end time are provided."""
        if self.user.get_current_user():
            if self.start_time and self.end_time:
                try:
                    self.user.cursor.execute(
                        'INSERT INTO study_sessions (user_id, subject_id, start_time, end_time, session_date) VALUES (%s, %s, %s, %s, %s)',
                        (self.user.id, self.subject.get_subject()["subject"]["subject_id"], self.start_time, self.end_time, self.start_time.date()) 
                    )

                    studied_mins = (self.end_time - self.start_time).seconds // 60 

                    self.user.cursor.execute(
                        'UPDATE subjects SET studied_mins = studied_mins + %s WHERE user_id = %s AND subject_id = %s',
                        (studied_mins, self.user.id, self.subject.get_subject()["subject"]["subject_id"])
                    )

                    self.user.connection.commit() 
                    return {"successful": True, "message": "Session recorded"}
                except Exception as e:
                    print("Exception adding session", str(e))
                    return {"successful": False, "message": str(e)}
            else:
                print("Start and end time must be provided")
                return {"successful": False, "message": "Start and end time must be provided"}
        else:
            print("User not found")
            return {"successful": False, "message": "User not found"}
