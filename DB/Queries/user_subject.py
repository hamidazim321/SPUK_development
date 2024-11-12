from DB.Database import Database


class UserSubject(Database):
    # Schema (
    # username TEXT NOT NULL,
    # subject_name TEXT NOT NULL,
    # current_chapter INTEGER,
    # total_chapters INTEGER,
    # studied_mins INTEGER DEFAULT 0,
    # FOREIGN KEY(username) REFERENCES users(username),
    # PRIMARY KEY(username, subject_name)
    # )

    def __init__(self, subject_name: str):
        super().__init__()
        self.subject_name = subject_name
        self.current_user = self.get_logged_in_user()

    def add_subject(self, total_chapters, current_chapter) -> dict:
        """Add a subject for the current user."""
        if self.current_user:
            try:
                self.cursor.execute(
                    '''
                    INSERT INTO user_subjects (subject_name, username, total_chapters, current_chapter) 
                    VALUES (?, ?, ?, ?)
                    ''',
                    (self.subject_name,
                     self.current_user.username, total_chapters, current_chapter)
                )
                self.commit()

                # Fetch the newly inserted subject
                self.cursor.execute(
                    '''
                    SELECT subject_name, total_chapters, current_chapter, studied_mins
                    FROM user_subjects 
                    WHERE subject_name = ? AND username = ?
                    ''',
                    (self.subject_name, self.current_user.username)
                )
                subject_added = self.cursor.fetchone()

                return {
                    "successful": True,
                    "subject": {
                        "subject_name": subject_added[0],
                        "total_chapters": subject_added[1],
                        "current_chapter": subject_added[2],
                        "studied_mins": subject_added[3]
                    }
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
        if self.current_user:
            try:
                self.cursor.execute(
                    '''
                    DELETE FROM user_subjects 
                    WHERE subject_name = ? AND username = ?
                    ''',
                    (self.subject_name, self.current_user.username)
                )
                self.commit()
                return {"successful": True}
            except Exception as e:
                self.connection.rollback()
                print("Error removing subject:", str(e))
                return {"successful": False, "message": str(e)}
        else:
            print("User not found")
            return {"successful": False, "message": "User not found"}

    def get_all_subjects(self) -> dict:
        """Retrieve all subjects for the current user."""
        if self.current_user:
            try:
                self.cursor.execute(
                    '''
                    SELECT subject_name, current_chapter, total_chapters, studied_mins 
                    FROM user_subjects 
                    WHERE username = ?
                    ''',
                    (self.current_user.username,)
                )
                subjects = self.cursor.fetchall()
                subjects_list = [
                    {
                        "subject_name": s[0],
                        "current_chapter": s[1],
                        "total_chapters": s[2],
                        "studied_mins": s[3]
                    }
                    for s in subjects
                ]
                return {"successful": True, "subjects": subjects_list}
            except Exception as e:
                print("Error fetching subjects:", str(e))
                return {"successful": False, "message": str(e)}
        else:
            print("User not found")
            return {"successful": False, "message": "User not found"}

    def get_subject(self) -> dict:
        """Retrieve details for this subject."""
        if self.current_user:
            try:
                self.cursor.execute(
                    '''
                    SELECT subject_name, current_chapter, total_chapters, duration_mins 
                    FROM user_subjects 
                    WHERE username = ? AND subject_name = ?
                    ''',
                    (self.current_user.username, self.subject_name)
                )
                subject = self.cursor.fetchone()

                if subject:
                    return {
                        "successful": True,
                        "subject": {
                            "subject_name": subject[0],
                            "current_chapter": subject[1],
                            "total_chapters": subject[2],
                            "studied_mins": subject[3]
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
