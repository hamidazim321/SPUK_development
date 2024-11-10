import sqlite3


class Database:
    def __init__(self):
        self.__current_user = None
        try:
            self.connection = sqlite3.connect("spuk.db")
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON")
            self.__create_tables()
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self.connection = None

    def __create_tables(self):
        # Create users table
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY UNIQUE NOT NULL,
                password_digest TEXT NOT NULL
            )
        """)
            self.connection.commit()
            print("users table created or already exists.")
        except sqlite3.Error as e:
            print(f"Error creating users table: {e}")

        # Create subjects table
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_subjects (
                username TEXT NOT NULL,
                subject_name TEXT NOT NULL,
                current_chapter INTEGER,
                total_chapters INTEGER,
                duration_mins INTEGER DEFAULT 0,
                FOREIGN KEY (username) REFERENCES users(username),
                PRIMARY KEY (username, subject_name)
            )
        """)
            self.connection.commit()
            print("subjects table created or already exists.")
        except sqlite3.Error as e:
            print(f"Error creating subjects table: {e}")

        # Create study_sessions table
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time DATETIME NOT NULL,
                end_time DATETIME NOT NULL,
                duration_mins INTEGER NOT NULL,
                username TEXT NOT NULL,
                subject_name TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES users(username),
                FOREIGN KEY (username, subject_name) REFERENCES user_subjects(username, subject_name)
            )
        """)
            self.connection.commit()
            print("study_sessions table created or already exists.")
        except sqlite3.Error as e:
            print(f"Error creating study_sessions table: {e}")

        # Create user_goals table
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                username TEXT NOT NULL,
                due_date DATE NOT NULL,
                achieved INTEGER CHECK(achieved IN (0, 1)),
                expired INTEGER CHECK(expired IN (0, 1)),
                FOREIGN KEY (username) REFERENCES users(username)
            )
        """)
            self.connection.commit()
            print("user_goals table created or already exists.")
        except sqlite3.Error as e:
            print(f"Error creating user_goals table: {e}")

        # Create user_exams table
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                subject_name TEXT NOT NULL,
                title TEXT NOT NULL,
                exam_date DATE NOT NULL,
                FOREIGN KEY (username) REFERENCES users(username),
                FOREIGN KEY (username, subject_name) REFERENCES user_subjects(username, subject_name)
            )
        """)
            self.connection.commit()
            print("user_exams table created or already exists.")
        except sqlite3.Error as e:
            print(f"Error creating user_exams table: {e}")

    def commit(self):
        if self.connection:
            try:
                self.connection.commit()
                print("Transaction committed successfully.")
            except Exception as e:
                print(f"Error committing transaction: {e}")

        def close(self):
            if self.connection:
                self.cursor.close()
                self.connection.close()
                print("Database connection closed.")

        def set_current_user(self, user):
            self.__current_user = user

        def get_current_user(self):
            return self.__current_user

        def remove_current_user(self):
            self.__current_user = None
