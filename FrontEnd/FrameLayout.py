from customtkinter import *
from StartSessionPage import StartSessionPage
from SubjectsPage import SubjectsPage
from StateManager import StateManager

class FrameLayout(CTkFrame): 
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager

        self.tabview = CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)

        self.tabview.add("Subjects")
        self.tabview.add("Session")
        self.tabview.add("Logout")
        self.tabview.set("Subjects")

        self.subjects_page = SubjectsPage(self.tabview.tab("Subjects"), self.state_manager)
        self.session_page = StartSessionPage(self.tabview.tab("Session"), self.state_manager)

        self.logout_btn = CTkButton(self.tabview.tab("Logout"), text="Logout", command=self.logout)
        self.logout_btn.pack(pady=10)

    def logout(self):
        self.state_manager.set_state({"is_logged_in": False})
