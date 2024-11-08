import tkinter as tk
from tkinter import ttk
from tkinter import Frame
from tkinter import messagebox
from datetime import datetime
import time  
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB.Tables.sessions import Session
from DB.Tables.subjects import Subject

class StartSessionPage(Frame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        self.user = self.state_manager.get_state()["user"]
        self.set_global_session()
        self.state = self.state_manager.get_state()
        self.user_subjects = self.get_user_subjects()
        self.current_session = self.state["current_session"]


        self.load_page()

    def set_global_session(self):
        session = Session(self.user, "")
        self.state_manager.set_state({"current_session": session})
    
    def get_user_subjects(self):
        subject = Subject(self.user, "")
        req = subject.get_all_subjects()
        if req["successful"]:
            return req["subjects"]
        else:
            messagebox.showerror("Error loading subjects", req["message"])

    def load_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        subframe = tk.Frame(self)
        subframe.pack(expand=True, fill="both")

        subject_options = [f"{subject['subject_name']} ({subject['id']})" for subject in self.user_subjects]
        subjects_selector = ttk.Combobox(subframe, values=subject_options, state="readonly")
        subjects_selector.set("Select subject")
        subjects_selector.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

        start_session_btn = tk.Button(
            subframe, 
            text="Start Session", 
            font=("Arial", 12, "bold"), 
            bg="blue", 
            fg="white",
            padx=20, 
            pady=10,
            command=self.start_session
        )
        start_session_btn.config(borderwidth=5, relief="ridge") 
        start_session_btn.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        end_session_btn = tk.Button(
            subframe, 
            text="End Session", 
            font=("Arial", 12, "bold"), 
            bg="red", 
            fg="white",
            padx=20, 
            pady=10,
            command=self.end_session
        )
        end_session_btn.config(borderwidth=5, relief="ridge")
        end_session_btn.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

        if self.current_session.start_time:
            start_session_btn.config(state="disabled")
        if self.current_session.end_time:
            end_session_btn.config(state="disabled")

    def start_session(self):
        self.current_session.start_session() 
        self.state_manager.set_state({"current_session": self.current_session})
        self.load_page()

    def end_session(self):
        self.current_session.end_session()
        self.state_manager.set_state({"current_session": self.current_session})
        self.load_page()
        print(self.current_session.duration_mins)

    def add_session(self):
        return
    
    def cancel_session(self):
        return
