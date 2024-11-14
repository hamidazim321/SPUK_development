from DB.Database import Database


class UserSubject(Database):
    # Schema (
        # id INTEGER PRIMARY KEY AUTOINCREMENT,
        # user_id INTEGER NOT NULL,
        # subject_name TEXT NOT NULL,
        # current_chapter INTEGER,
        # total_chapters INTEGER,
        # studied_mins INTEGER DEFAULT 0,
        # FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    # )

    def __init__(self, subject_name: str, id=None, current_chapter=None, total_chapters=None):
        super().__init__()
        self.subject_name = subject_name
        self.current_user = self.get_logged_in_user()
        self.id = id
        self.current_chapter = current_chapter
        self.total_chapters = total_chapters
        self.studied_mins = 0

    def add_subject(self) -> dict:
        """Add a subject for the current user."""
        if self.current_user:
            try:
                self.cursor.execute(
                    '''
                    INSERT INTO user_subjects (subject_name, user_id, total_chapters, current_chapter) 
                    VALUES (?, ?, ?, ?)
                    ''',
                    (self.subject_name, self.current_user.id, self.total_chapters, self.current_chapter)
                )
                self.commit()

                # Fetch the newly inserted subject
                self.cursor.execute(
                    '''
                    SELECT subject_name, total_chapters, current_chapter, id
                    FROM user_subjects 
                    WHERE subject_name = ? AND user_id = ?
                    ORDER BY id DESC
                    LIMIT 1
                    ''',
                    (self.subject_name, self.current_user.id)
                )
                subject_added = self.cursor.fetchone()
                self.total_chapters = subject_added[1]
                self.current_chapter = subject_added[2]
                self.id = subject_added[3]

                return {
                    "successful": True,
                }
            except Exception as e:
                self.connection.rollback()
                print("Error creating subject:", str(e))
                return {"successful": False, "message": str(e)}
        else:
            print("User not found")
            return {"successful": False, "message": "User not found"}

    def remove_subject(self) -> dict:
        """Remove a subject for the current user."""
        if self.current_user and self.id:
            try:
                self.cursor.execute(
                    '''
                    DELETE FROM user_subjects 
                    WHERE id = ? AND user_id = ?
                    ''',
                    (self.id, self.current_user.id)
                )
                self.commit()
                return {"successful": True}
            except Exception as e:
                self.connection.rollback()
                print("Error removing subject:", str(e))
                return {"successful": False, "message": str(e)}
        else:
            print("User or subject not found")
            return {"successful": False, "message": "User or subject not found"}

    def get_all_subjects(self) -> dict:
        """Retrieve all subjects for the current user."""
        if self.current_user:
            try:
                self.cursor.execute(
                    '''
                    SELECT subject_name, id, current_chapter, total_chapters, studied_mins
                    FROM user_subjects 
                    WHERE user_id = ?
                    ''',
                    (self.current_user.id,)
                )
                subjects = self.cursor.fetchall()
                subjects_list = []
                for s in subjects:
                    subj = UserSubject(s[0], s[1], s[2], s[3])
                    subj.studied_mins = s[4]
                    subjects_list.append(subj)
                return {"successful": True, "subjects": subjects_list}
            except Exception as e:
                print("Error fetching subjects:", str(e))
                return {"successful": False, "message": str(e)}
        else:
            print("User not found")
            return {"successful": False, "message": "User not found"}
