import tkinter as tk
from tkinter import Frame

class RegistrationPage(Frame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        self.load_page()
    
    def load_page(self):
        subframe = tk.Frame(self)
        label = tk.Label(subframe, text="Registration page")
        label.pack()

        # Pack the subframe
        subframe.pack(expand=True, fill="both")