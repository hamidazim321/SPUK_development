from DB.Tables.users import User

class Subject:
    def __init__(self, user: User, subject_name):
        self.user = user
        self.subject_name = subject_name
    

    def add_subject(self, total_chapters, current_chapter) -> dict:
        if self.user.get_current_user(): 
            try:
                self.user.cursor.execute(
                    'INSERT INTO subjects (subject_name, user_id, total_chapters, current_chapter, studied_mins) VALUES (%s, %s, %s, %s, %s)',
                    (self.subject_name, self.user.get_current_user().id, total_chapters, current_chapter, 0)
                )
                self.user.connection.commit()
                return {"successful": True, 
                "subject": {
                    "subject_name": self.subject_name,
                    "current_chapter": current_chapter,
                    "total_chapters": total_chapters,
                    "studied_mins": 0
                    }
                }
            except Exception as e:
                self.user.connection.rollback()
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
                self.user.connection.rollback()
                print("Error removing subject:", str(e))
                return {"successful": False, "message": str(e)}
        else:
            print("User not found")
            return {"successful": False, "message": "User not found"}

    def get_all_subjects(self) -> dict:
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

    def get_subject(self) -> dict:
      """Retrieve this subject details."""
      if self.user.get_current_user():
          try:
              self.user.cursor.execute(
                  'SELECT subject_name, current_chapter, total_chapters, studied_mins, subject_id FROM subjects WHERE user_id = %s AND subject_name = %s',
                  (self.user.get_current_user().id, self.subject_name)
              )
              subject = self.user.cursor.fetchone()

              if subject:
                  return {
                      "successful": True,
                      "subject": {
                          "subject_name": subject[0],
                          "current_chapter": subject[1],
                          "total_chapters": subject[2],
                          "studied_mins": subject[3],
                          "subject_id": subject[4]
                      }
                  }
              else:
                  return {"successful": False, "message": "Subject not found"}

          except Exception as e:
              print("Error fetching subject:", str(e))
              return {"successful": False, "message": str(e)}
      else:
          print("User not found")
          return {"successful": False, "message": "User not found"}
