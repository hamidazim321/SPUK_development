from DB.Database import Database

class UserGoal(Database):
  # Schema(
  #   id INTEGER PRIMARY KEY AUTOINCREMENT,
  #   title TEXT NOT NULL,
  #   description TEXT NOT NULL,
  #   user_id INTEGER NOT NULL,
  #   due_date DATE NOT NULL,
  #   achieved INTEGER NOT NULL DEFAULT 0,
  #   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  #   CHECK(achieved IN (0, 1)),
  #   CHECK(expired IN (0, 1))
  # )

  def __init__(self, title=None, description=None, due_date=None, achieved=0):
      super().__init__()
      self.title = title
      self.description = description
      self.due_date = due_date
      self.achieved = achieved
      self.current_user = self.get_logged_in_user()
      self.id = None

  def add_goal(self) -> dict:
    """Add a new goal for the current user."""
    if self.current_user:
      try:
        self.cursor.execute(
            '''
            INSERT INTO user_goals (title, description, user_id, due_date, achieved) 
            VALUES (?, ?, ?, ?, ?)
            ''',
            (self.title, self.description, self.current_user.id, self.due_date, self.achieved)
        )
        self.commit()

        self.id = self.cursor.lastrowid

        return {"successful": True}
      except Exception as e:
        self.connection.rollback()
        print("Error creating goal:", str(e))
        return {"successful": False, "message": str(e)}
    else:
      print("User not found")
      return {"successful": False, "message": "User not found"}

  def remove_goal(self) -> dict:
    """Remove a goal for the current user."""
    if self.current_user and self.id:
      try:
        self.cursor.execute(
            '''
            DELETE FROM user_goals 
            WHERE id = ? AND user_id = ?
            ''',
            (self.id, self.current_user.id)
        )
        self.commit()
        return {"successful": True}
      except Exception as e:
        self.connection.rollback()
        print("Error removing goal:", str(e))
        return {"successful": False, "message": str(e)}
    else:
      print("User or goal not found")
      return {"successful": False, "message": "User or goal not found"}

  def get_all_goals(self) -> dict:
    """Retrieve all goals for the current user."""
    if self.current_user:
      try:
        self.cursor.execute(
            '''
            SELECT id, title, description, due_date, achieved
            FROM user_goals 
            WHERE user_id = ?
            ''',
            (self.current_user.id,)
        )
        goals = self.cursor.fetchall()
        goals_list = []
        for g in goals:
          goal = UserGoal(g[1], g[2], g[3], g[4])
          goal.id = g[0]
          goals_list.append(goal)
            
        return {"successful": True, "goals": goals_list}
      except Exception as e:
        print("Error fetching goals:", str(e))
        return {"successful": False, "message": str(e)}
    else:
      print("User not found")
      return {"successful": False, "message": "User not found"}

  def update_goal(self) -> dict:
    """Update an existing goal for the current user."""
    if self.current_user and self.id:
      try:
        self.cursor.execute(
            '''
            UPDATE user_goals
            SET title = ?, description = ?, due_date = ?, achieved = ?
            WHERE id = ? AND user_id = ?
            ''',
            (self.title, self.description, self.due_date, self.achieved, self.id, self.current_user.id)
        )
        self.commit()
        return {"successful": True}
      except Exception as e:
        self.connection.rollback()
        print("Error updating goal:", str(e))
        return {"successful": False, "message": str(e)}
    else:
        print("User or goal not found")
        return {"successful": False, "message": "User or goal not found"}
