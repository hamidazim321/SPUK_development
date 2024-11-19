from customtkinter import CTkScrollableFrame, CTkFrame, CTkLabel
from CTkMessagebox import CTkMessagebox
from datetime import datetime
from DB.Queries.study_session import StudySession
from DB.Queries.user_subject import UserSubject

class SessionsPage(CTkScrollableFrame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        self.session_table = None
        self.load_page()

    def destroy(self):
        self.state_manager.unsubscribe(self)
        super().destroy()

    def load_page(self):
        self.session_table = SessionsTable(self, self.state_manager)
        self.session_table.pack()
  

# Dynamic components

class SessionsTable(CTkFrame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        self.user_sessions = self.__fetch_user_sessions()
        self.state_manager.set_state({"user_sessions": self.user_sessions})
        self.user_subjects_to_id = self.__fetch_user_subject_to_id()

        self.state_manager.subscribe(self.__update_user_subjects, ["user_subjects"], self)
        self.state_manager.subscribe(self.__update_session_table, ["user_sessions"], self)

        self.columnconfigure([0, 1, 2, 3, 4], weight=1)
        self.configure(border_width=2, border_color="gray")

        self.__table_headers = ["Subject", "Date", "Start time", "End time", "Duration"]
        
        for idx, col in enumerate(self.__table_headers):
            CTkLabel(self, text=col, font=("Arial", 16, "bold"), anchor="center", padx=10, pady=5).grid(column=idx, row=0, sticky="ew", padx=5, pady=5)
        
        for row_idx, session in enumerate(self.user_sessions, 1):
            self.__add_session(session, row_idx)
    
    def __update_session_table(self, state):
        new_session = None
        if state["user_sessions"]:
            new_session = state["user_sessions"][-1]
        if new_session:
            for widget in self.winfo_children():
                info = widget.grid_info()
                if info["row"] == 0:
                    continue
                widget.grid(row=info["row"] + 1, column=info["column"])
            self.__add_session(new_session, 1)
            self.user_sessions.insert(0, new_session)

    
    def __add_session(self, session, row):
        hours, minutes = divmod(session.duration_mins, 60)
        start_time_formatted = session.start_time.strftime("%H:%M")
        end_time_formatted = session.end_time.strftime("%H:%M")
        date_formatted = session.start_time.strftime("%d,%B,%Y")
        
        CTkLabel(self, text=self.user_subjects_to_id.get(session.subject_id, "Unknown Subject"),
                 font=("Arial", 14), anchor="w", padx=10, pady=5).grid(row=row, column=0, sticky="w", padx=5, pady=5)
        CTkLabel(self, text=date_formatted, font=("Arial", 14), anchor="w", padx=10, pady=5).grid(row=row, column=1, sticky="w", padx=5, pady=5)
        CTkLabel(self, text=start_time_formatted, font=("Arial", 14), anchor="w", padx=10, pady=5).grid(row=row, column=2, sticky="w", padx=5, pady=5)
        CTkLabel(self, text=end_time_formatted, font=("Arial", 14), anchor="w", padx=10, pady=5).grid(row=row, column=3, sticky="w", padx=5, pady=5)
        CTkLabel(self, text=f"{hours} hours, {minutes} mins", font=("Arial", 14), anchor="w", padx=10, pady=5).grid(row=row, column=4, sticky="w", padx=5, pady=5)

    def __fetch_user_subject_to_id(self):
        subject = UserSubject("")
        req = subject.get_subject_to_id()
        if req["successful"]:
            return req["subjects"]
        else:
            CTkMessagebox(title="Error fetching subjects", message=req["message"], icon="cancel")
            return {}

    def __fetch_user_sessions(self):
        session = StudySession()
        try:
            req = session.get_user_sessions()
            if req["successful"]:
                return req["sessions"]
            else:
              CTkMessagebox(title="Error fetching sessions", message=req["message"], icon="cancel")
              return []
        except Exception as e:  
            CTkMessagebox(title="Error getting sessions", message=str(e), icon="cancel")
            return []
    
    def __update_user_subjects(self, state):
        self.user_subjects_to_id = self.__fetch_user_subject_to_id()
                