from DB.Tables.users import User

class Subject:
    def __init__(self, user: User, subject_name):
        self.user = user
        self.subject_name = subject_name

    def add_subject(self, total_chapters, current_chapter, studied_mins=0) -> dict:
        if self.user.get_current_user(): 
            try:
                self.user.cursor.execute(
                    'INSERT INTO subjects (subject_name, user_id, total_chapters, current_chapter, studied_mins) VALUES (%s, %s, %s, %s, %s)',
                    (self.subject_name, self.user.get_current_user().id, total_chapters, current_chapter, studied_mins)
                )
                self.user.connection.commit()
                return {"successful": True}
            except Exception as e:
                print("Error creating subject:", str(e))
                return {"successful": False, "message": str(e)}
        else:
            print("User not found")
            return {"successful": False, "message": "User not found"}
    
    def remove_subject(self) -> dict:
        if self.user.get_current_user():
            try:
                self.user.cursor.execute(
                    'DELETE FROM subjects WHERE subject_name = %s AND user_id = %s',
                    (self.subject_name, self.user.get_current_user().id)
                )
                self.user.connection.commit()
                return {"successful": True}
            except Exception as e:
                print("Error removing subject:", str(e))
                return {"successful": False, "message": str(e)}
        else:
            print("User not found")
            return {"successful": False, "message": "User not found"}

    def get_user_subjects(self) -> dict:
        if self.user.get_current_user():
            try:
                self.user.cursor.execute(
                    'SELECT subject_name, current_chapter, total_chapters, studied_mins FROM subjects WHERE user_id = %s',
                    (self.user.get_current_user().id,)
                )
                subjects = self.user.cursor.fetchall()
                subjects_object = []
                for s in subjects:
                    subjects_object.append({
                        "subject_name": s[0],
                        "current_chapter": s[1],
                        "total_chapters": s[2],
                        "studied_mins": s[3]
                    })
                print("Subjects fetched")
                return {"successful": True, "subjects": subjects_object}
            except Exception as e:
                print("Error fetching subjects:", str(e))
                return {"successful": False, "message": str(e)}
        else:
            print("User not found")
            return {"successful": False, "message": "User not found"}
