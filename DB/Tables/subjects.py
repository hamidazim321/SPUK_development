from DB.connectDB import Database
from DB.Tables.users import User

class Subject(Database):
  def __init__(self, subject_name, user_id):
    super().__init__()
    self.subject_name = subject_name
    self.user_id = user_id

  def add_subject(self, total_chapters, current_chapter, studied_mins=0) -> dict:
    try:
      self.cursor.execute('INSERT INTO subjects (subject_name, user_id, total_chapters, current_chapter, studied_mins VALUES (%s,%s,%s,%s,%s,))',
      (self.subject_name, self.user_id, total_chapters, current_chapter, studied_mins)
      )
      self.connection.commit()
      return {"successful": True}
    except Exception as e:
      print("Error creating subject", str(e))
      return {"successful": False, "message": str(e)}
  
