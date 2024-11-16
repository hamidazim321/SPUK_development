import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import re
from customtkinter import CTk
from FrameLayout import FrameLayout
from LoginPage import LoginPage
from StateManager import StateManager
from DB.Database import Database
class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Sabaq pa Usul Ke")
        self.geometry('600x600')

        # State Management
        self.state_manager = StateManager()
        self.logged_in = self.state_manager.get_state()["is_logged_in"]
        self.state_manager.subscribe(self.update_home_page, ["is_logged_in"], self)

        # Initialize layout
        self.current_frame = None
        self.load_home_page()

        # Bind window close event to the `on_closing` method
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_frame(self, frame_class):
        # Destroy the current frame if it exists
        if self.current_frame is not None:
            self.current_frame.destroy()

        # Initialize the new frame
        self.current_frame = frame_class(self, self.state_manager)
        self.current_frame.pack(fill="both", expand=True)

    def load_home_page(self):
        if self.logged_in:
            self.show_frame(FrameLayout)
        else:
            self.show_frame(LoginPage)

    def update_home_page(self, state):
        self.logged_in = state["is_logged_in"]
        self.load_home_page()

    def on_closing(self):
        Database.close()
        self.destroy()

app = App()
app.mainloop()
