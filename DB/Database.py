import sqlite3


class Database:
    connection = None
    cursor = None
    __logged_in_user = None

    def __init__(self):
        if Database.connection is None:
            try:
                Database.connection = sqlite3.connect("spuk.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
                Database.cursor = Database.connection.cursor()
                Database.cursor.execute("PRAGMA foreign_keys = ON")
                self.__create_tables()
            except Exception as e:
                print(f"Error connecting to the database: {e}")
                Database.connection = None
        self.connection = Database.connection
        self.cursor = Database.cursor

    def __create_tables(self):
        # Create users table
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_digest TEXT NOT NULL
            )
            """)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating users table: {e}")

        # Create subjects table
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                subject_name TEXT NOT NULL,
                current_chapter INTEGER,
                total_chapters INTEGER,
                studied_mins INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                CHECK (current_chapter <= total_chapters)
            )
            """)
            self.connection.commit()
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
                user_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES user_subjects(id) ON DELETE CASCADE
            )
            """)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating study_sessions table: {e}")

        # Create user_goals table
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                due_date DATE NOT NULL,
                achieved INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                CHECK(achieved IN (0, 1))
            )
            """)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating user_goals table: {e}")

        # Create user_exams table
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                exam_date DATE NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES user_subjects(id) ON DELETE CASCADE
            )
            """)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating user_exams table: {e}")

    def commit(self):
        if self.connection:
            try:
                self.connection.commit()
            except Exception as e:
                print(f"Error committing transaction: {e}")
		
		
    @classmethod
    def close(cls):
        if cls.connection:
            cls.cursor.close()
            cls.connection.close()

    @classmethod
    def set_logged_in_user(cls, user):
        cls.__logged_in_user = user

    @classmethod
    def get_logged_in_user(cls):
        return cls.__logged_in_user

    @classmethod
    def remove_logged_in_user(cls):
        cls.__logged_in_user = None
