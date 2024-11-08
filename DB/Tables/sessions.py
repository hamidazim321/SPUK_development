from DB.Tables.users import User
from DB.Tables.subjects import Subject
import datetime

class Session:
    def __init__(self, user: User, start_time=None, end_time=None):
        self.user = user
        self.start_time = start_time
        self.end_time = end_time
        self.duration_mins = None

    def start_session(self):
        """Set start_time to the current timestamp."""
        if self.user.get_current_user():
            self.start_time = datetime.datetime.now()
            print(f"Session started at {self.start_time}")
        else:
            print("User not found")
            return False
    
    def end_session(self):
        """Set end_time to the current timestamp."""
        if self.user.get_current_user():
            self.end_time = datetime.datetime.now()
            print(f"Session ended at {self.end_time}")
            self.duration_mins = (self.end_time - self.start_time).seconds // 60
        else:
            print("User not found")
            return False

    def add_session(self, subject_id):
        """Add session details if start and end time are provided."""
        if self.user.get_current_user():
            if self.start_time and self.end_time:
                try:
                    self.user.cursor.execute(
                        '''
                        INSERT INTO study_sessions (user_id, subject_id, start_time, end_time, session_date, duration_mins) VALUES (%s, %s, %s, %s, %s)
                        RETURNING session_id, subject_id, start_time, end_time, session_date, duration_mins
                        ''',
                        (self.user.id, subject_id, self.start_time, self.end_time, self.start_time.date(), self.duration_mins) 
                    )
 
                    session_added = self.cursor.fetchone()

                    self.user.cursor.execute(
                        'UPDATE subjects SET studied_mins = studied_mins + %s WHERE user_id = %s AND subject_id = %s',
                        (studied_mins, self.user.id, subject_id)
                    )

                    self.user.connection.commit() 
                    return {
                        "successful": True, 
                        "session":{
                            "id": session_added[0],
                            "subject_id": session_added[1],
                            "start_time": session_added[2],
                            "end_time": session_added[3],
                            "session_date": session_added[4],
                            "duration_mins": session_added[5]
                        }
                        }
                    self.reset_session()
                except Exception as e:
                    print("Exception adding session", str(e))
                    return {"successful": False, "message": str(e)}
            else:
                print("Start and end time must be provided")
                return {"successful": False, "message": "Start and end time must be provided"}
        else:
            print("User not found")
            return {"successful": False, "message": "User not found"}
    
    def reset_session(self):
        self.start_time = None
        self.end_time = None
        self.duration_mins = None
    
