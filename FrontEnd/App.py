import tkinter as tk
from tkinter import Frame
from Menu import Menu
from LoginPage import LoginPage
from RegistrationPage import RegistrationPage
from StartSessionPage import StartSessionPage
from ViewSubjectsPage import ViewSubjectsPage
from StateManager import StateManager


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sabaq pa Usul Ke")
        self.geometry('600x600')

        # State Management
        self.state_manager = StateManager()
        self.state_manager.subscribe(self.load_home_page)

        # pages
        self.pages = [
            {"page": ViewSubjectsPage, "name": "Subjects"},
            {"page": StartSessionPage, "name": "Sessions"},
        ]

        # Initialize Menu first to keep it on top
        self.menu = Menu(self, self.state_manager, self.show_frame, self.pages)
        self.menu.pack(side="top", fill='x')

        # initialize home page
        self.current_frame = None
        self.load_home_page(self.state_manager.get_state())

    def show_frame(self, page):
        # Destroy the current frame if it exists
        if self.current_frame is not None:
            self.current_frame.destroy()
        
        # Initialize the new frame
        self.current_frame = page(self, self.state_manager)
        
        # Pack the new frame
        self.current_frame.pack(fill='both', expand=True)
        print("Page loaded:", page.__name__)
    
    def load_home_page(self, state):
        if state["is_logged_in"]:
            self.show_frame(ViewSubjectsPage)
        else:
            self.show_frame(LoginPage)
        

        

app = App()
app.mainloop()
