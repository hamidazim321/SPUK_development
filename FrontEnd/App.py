import tkinter as tk
from tkinter import Frame
from Menu import Menu
from LoginPage import LoginPage
from RegistrationPage import RegistrationPage
from StartSessionPage import StartSessionPage
from SubjectsPage import SubjectsPage
from StateManager import StateManager


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sabaq pa Usul Ke")
        self.geometry('600x600')

        # State Management
        self.state_manager = StateManager()
        self.logged_in = self.state_manager.get_state()["is_logged_in"]
        self.state_manager.subscribe(self.update_home_page)

        # pages
        self.pages = [
            {"page": SubjectsPage, "name": "Subjects"},
            {"page": StartSessionPage, "name": "Sessions"},
        ]

        # Initialize Menu first to keep it on top
        self.menu = Menu(self, self.state_manager, self.show_frame, self.pages)
        self.menu.pack(side="top", fill='x')

        # initialize home page
        self.current_frame = None
        self.load_home_page()

    def show_frame(self, page):
        # Destroy the current frame if it exists
        if self.current_frame is not None:
            self.current_frame.destroy()
        
        # Initialize the new frame
        self.current_frame = page(self, self.state_manager)
        
        # Pack the new frame
        self.current_frame.pack(fill='both', expand=True)
    
    def load_home_page(self):
        if self.logged_in:
            self.show_frame(SubjectsPage)
        else:
            self.show_frame(LoginPage)
    
    def update_home_page(self, state):
        if self.logged_in == state["is_logged_in"]:
            return
        else:
            self.logged_in = state["is_logged_in"]
            self.load_home_page()

        

        

app = App()
app.mainloop()
