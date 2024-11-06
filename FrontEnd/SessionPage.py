import tkinter as tk
from tkinter import Frame

class SessionPage(Frame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        self.load_page()
        self.state = self.state_manager.get_state()
    
    def load_global_session(self):
        # Add a Session object to global state if its None
        return
    
    def load_page(self):
        subframe = tk.Frame(self)
        label = tk.Label(subframe, text="Session page")
        label.pack()

        # Pack the subframe
        subframe.pack(expand=True, fill="both")

    def fetch_sessions(self):
        # Fetch sessions from DB and return array of sessions
        return

    def start_session(self):
        # add start time current session and save it in global state
        return

    def end_session(self):
        # add end time to the session in global state
        return

    def add_session(self):
        return
    
    def cancel_session(self):
        return
