import tkinter as tk
from tkinter import Frame

class StartSessionPage(Frame):
    def __init__(self, master):
        super().__init__(master)
        label = tk.Label(self, text="Start Session Page")
        label.pack()