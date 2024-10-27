import tkinter as tk
from tkinter import Frame

class ViewSubjectsPage(Frame):
    def __init__(self, master):
        super().__init__(master)
        label = tk.Label(self, text="View Subjects Page")
        label.pack()
