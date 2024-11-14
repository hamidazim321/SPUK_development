import os
import sys
import re
from tkinter import messagebox
from tkinter import Frame
from tkinter import ttk
import tkinter as tk
from Components.Timer import Timer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB.Queries.user_subject import UserSubject
from DB.Queries.study_session import StudySession

class StartSessionPage(Frame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        self.state = self.state_manager.get_state()
        self.set_global_session()
        self.user_subjects = self.get_user_subjects()
        self.subject_options = [subject.subject_name for subject in self.user_subjects]
        self.current_session = self.state["current_session"]

        self.load_page()

    def set_global_session(self):
        if self.state["current_session"] == None:
            session = StudySession()
            self.state_manager.set_state({"current_session": session})
            self.state["current_session"] = session
    def get_user_subjects(self):
        subject = UserSubject("")
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

        subjects_selector = ttk.Combobox(
            subframe, values=self.subject_options, state="readonly")
        subjects_selector.set("Select subject")
        subjects_selector.grid(row=0, column=0, padx=10,
                               pady=10, columnspan=2, sticky="ew")

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

        add_session_btn = tk.Button(
            subframe,
            text="add_session",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            padx=20,
            pady=10,
            command=lambda: self.add_session(
                subjects_selector.current())
        )
        add_session_btn.config(borderwidth=5, relief="ridge")

        timer_frame = tk.Frame(subframe)
        timer_frame.grid(row=3, column=0, columnspan=2)
        timer = Timer(timer_frame, self.current_session.start_time,
                      self.current_session.end_time)
        timer.pack()

        if not self.current_session.start_time:
            start_session_btn.grid(
                row=2, column=0, padx=10, pady=10, sticky="ew")
        elif self.current_session.start_time and not self.current_session.end_time:
            end_session_btn.grid(row=2, column=0, padx=10,
                                 pady=10, sticky="ew")
        else:
            add_session_btn.grid(row=2, column=0, padx=10,
                                 pady=10, sticky="ew")

    def start_session(self):
        self.current_session.start_session()
        self.state_manager.set_state({"current_session": self.current_session})
        self.load_page()

    def end_session(self):
        self.current_session.end_session()
        self.state_manager.set_state({"current_session": self.current_session})
        self.load_page()

    def add_session(self, subject_option_index:int):
        print(subject_option_index)
        if subject_option_index > -1:
            subject_id = self.user_subjects[subject_option_index].id
            self.current_session.subject_id = subject_id
            req = self.current_session.add_session()
            if req["successful"]:
                messagebox.showinfo("Session Added", f"Duration: {self.current_session.duration_mins} Minutes")
                user_sessions = self.state_manager.get_state()["user_sessions"]
                user_sessions.append(self.current_session)
                self.current_session = StudySession()
                self.state_manager.set_state({"user_sessions": user_sessions, "current_session": self.current_session})
                self.load_page()
            else:
                messagebox.showerror("Error adding session", req["message"])
        else:
            messagebox.showwarning("No Subject", "please select a subject")
