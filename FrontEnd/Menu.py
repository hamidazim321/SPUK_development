import tkinter as tk
from tkinter import Frame
from LoginPage import LoginPage
from RegistrationPage import RegistrationPage
from StartSessionPage import StartSessionPage
from ViewSubjectsPage import ViewSubjectsPage

class Menu(Frame):
    def __init__(self, master, show_frame_callback):
        super().__init__(master)
        self.show_frame_callback = show_frame_callback
        
        self.create_buttons()

    def create_buttons(self):

        login_button = tk.Button(self, text="Login", command=lambda: self.show_frame_callback(LoginPage))
        login_button.pack(side=tk.LEFT, padx=5, pady=5)

        register_button = tk.Button(self, text="Register", command=lambda: self.show_frame_callback(RegistrationPage))
        register_button.pack(side=tk.LEFT, padx=5, pady=5)

        view_subjects_button = tk.Button(self, text="View Subjects", command=lambda: self.show_frame_callback(ViewSubjectsPage))
        view_subjects_button.pack(side=tk.LEFT, padx=5, pady=5)

        start_session_button = tk.Button(self, text="Start Session", command=lambda: self.show_frame_callback(StartSessionPage))
        start_session_button.pack(side=tk.LEFT, padx=5, pady=5)

        logout_button = tk.Button(self, text="Logout", command=self.logout)
        logout_button.pack(side=tk.LEFT, padx=5, pady=5)

    def logout(self):
        print("User logged out")  
        self.show_frame_callback(LoginPage)

