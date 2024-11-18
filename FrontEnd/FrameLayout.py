from customtkinter import *
from StartSessionPage import StartSessionPage
from SubjectsPage import SubjectsPage
from UserSessionsPage import SessionsPage
from StateManager import StateManager

class FrameLayout(CTkFrame): 
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager

        self.tabview = CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)

        self.tabview.add("Subjects")
        self.tabview.add("Start Session")
        self.tabview.add("My Sessions")
        self.tabview.add("Logout")

        self.tabview.set("Subjects")

        self.subjects_page = SubjectsPage(self.tabview.tab("Subjects"), self.state_manager)
        self.user_sessions_page = SessionsPage(self.tabview.tab("My Sessions"), self.state_manager)
        self.start_session_page = StartSessionPage(self.tabview.tab("Start Session"), self.state_manager)

        self.subjects_page.pack(expand=True, fill="both")
        self.user_sessions_page.pack(expand=True, fill="both")
        self.start_session_page.pack(expand=True, fill="both")

        self.logout_btn = CTkButton(self.tabview.tab("Logout"), text="Logout", command=self.logout)
        self.logout_btn.pack(pady=10)

    def logout(self):
        self.state_manager.set_state({"is_logged_in": False})
    
