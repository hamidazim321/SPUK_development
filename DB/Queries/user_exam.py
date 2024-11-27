from DB.Database import Database

class UserExam(Database):
  # Schema(
  #   id INTEGER PRIMARY KEY AUTOINCREMENT,
  #   user_id INTEGER NOT NULL,
  #   subject_id INTEGER NOT NULL,
  #   title TEXT NOT NULL,
  #   exam_date DATE NOT NULL,
  #   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  #   FOREIGN KEY (subject_id) REFERENCES user_subjects(id) ON DELETE CASCADE
  # )

  def __init__(self, title=None, exam_date=None, subject_id=None):
      super().__init__()
      self.title = title
      self.exam_date = exam_date
      self.subject_id = subject_id
      self.current_user = self.get_logged_in_user()
      self.id = None

  def add_exam(self) -> dict:
    """Add a new exam for the current user."""
    if self.current_user:
      try:
        self.cursor.execute(
            '''
            INSERT INTO user_exams (title, exam_date, user_id, subject_id) 
            VALUES (?, ?, ?, ?)
            ''',
            (self.title, self.exam_date, self.current_user.id, self.subject_id)
        )
        self.commit()

        self.id = self.cursor.lastrowid

        return {"successful": True}
      except Exception as e:
        self.connection.rollback()
        print("Error creating exam:", str(e))
        return {"successful": False, "message": str(e)}
    else:
      print("User not found")
      return {"successful": False, "message": "User not found"}

  def remove_exam(self) -> dict:
    """Remove an exam for the current user."""
    if self.current_user and self.id:
      try:
        self.cursor.execute(
            '''
            DELETE FROM user_exams 
            WHERE id = ? AND user_id = ?
            ''',
            (self.id, self.current_user.id)
        )
        self.commit()
        return {"successful": True}
      except Exception as e:
        self.connection.rollback()
        print("Error removing exam:", str(e))
        return {"successful": False, "message": str(e)}
    else:
      print("User or exam not found")
      return {"successful": False, "message": "User or exam not found"}

  def get_all_exams(self) -> dict:
    """Retrieve all exams for the current user."""
    if self.current_user:
      try:
        self.cursor.execute(
            '''
            SELECT id, title, exam_date, subject_id
            FROM user_exams 
            WHERE user_id = ?
            ''',
            (self.current_user.id,)
        )
        exams = self.cursor.fetchall()
        exams_list = []

        for e in exams:
          exam = UserExam(e[1], e[2], e[3])
          exam.id = e[0]
          exams_list.append(exam)

        return {"successful": True, "exams": exams_list}
      except Exception as e:
        print("Error fetching exams:", str(e))
        return {"successful": False, "message": str(e)}
    else:
      print("User not found")
      return {"successful": False, "message": "User not found"}

  def update_exam(self) -> dict:
    """Update an existing exam for the current user."""
    if self.current_user and self.id:
      try:
        self.cursor.execute(
            '''
            UPDATE user_exams
            SET title = ?, exam_date = ?, subject_id = ?
            WHERE id = ? AND user_id = ?
            ''',
            (self.title, self.exam_date, self.subject_id, self.id, self.current_user.id)
        )
        self.commit()
        return {"successful": True}
      except Exception as e:
        self.connection.rollback()
        print("Error updating exam:", str(e))
        return {"successful": False, "message": str(e)}
    else:
      print("User or exam not found")
      return {"successful": False, "message": "User or exam not found"}
