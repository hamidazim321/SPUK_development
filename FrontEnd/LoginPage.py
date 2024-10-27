import tkinter as tk
from tkinter import Frame

class LoginPage(Frame):
    def __init__(self, master):
        super().__init__(master)
        label = tk.Label(self, text="Login Page")
        label.pack()