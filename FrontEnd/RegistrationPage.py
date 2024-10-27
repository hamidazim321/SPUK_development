import tkinter as tk
from tkinter import Frame

class RegistrationPage(Frame):
    def __init__(self, master):
        super().__init__(master)
        label = tk.Label(self, text="Registration Page")
        label.pack()