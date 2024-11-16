import os
import sys
import re
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkComboBox
from CTkMessagebox import CTkMessagebox
from Components.Timer import Timer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB.Queries.user_subject import UserSubject
from DB.Queries.study_session import StudySession


class StartSessionPage(CTkFrame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        self.state = self.state_manager.get_state()
        self.set_global_session()
        self.user_subjects = self.state["user_subjects"]
        self.subject_options = [f"{subject.subject_name}({subject.id})" for subject in self.user_subjects]
        self.current_session = self.state["current_session"]
        self.load_page()
        self.state_manager.subscribe(self.update_page)

    def set_global_session(self):
        if self.state["current_session"] is None:
            session = StudySession()
            self.state_manager.set_state({"current_session": session})
            self.state["current_session"] = session

    def update_page(self, state):
        print("update session Page called")
        if len(state["user_subjects"]) != len(self.user_subjects):
            print("session Page updated")
            self.state = state
            self.user_subjects = self.state["user_subjects"]
            self.subject_options = [f"{subject.subject_name}({subject.id})" for subject in self.user_subjects]
            self.load_page()

    def load_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        subframe = CTkFrame(self)
        subframe.pack(expand=True, fill="both", padx=20, pady=20)

        # Subject selector dropdown
        subjects_selector = CTkComboBox(
            subframe,
            values=self.subject_options,
            state="readonly",
        )
        subjects_selector.set("Select subject")
        subjects_selector.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

        # Start Session button
        start_session_btn = CTkButton(
            subframe,
            text="Start Session",
            command=self.start_session,
        )

        # End Session button
        end_session_btn = CTkButton(
            subframe,
            text="End Session",
            fg_color="red",
            hover_color="#ff4d4d",
            command=self.end_session,
        )

        # Add Session button
        add_session_btn = CTkButton(
            subframe,
            text="Add Session",
            fg_color="green",
            hover_color="#33cc33",
            command=lambda: self.add_session(subjects_selector.get()),
        )

        # Timer display
        timer_frame = CTkFrame(subframe)
        timer_frame.grid(row=3, column=0, columnspan=2, pady=10)
        timer = Timer(timer_frame, self.current_session.start_time, self.current_session.end_time)
        timer.pack()

        # Conditional button display
        if not self.current_session.start_time:
            start_session_btn.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        elif self.current_session.start_time and not self.current_session.end_time:
            end_session_btn.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        else:
            add_session_btn.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    def start_session(self):
        self.current_session.start_session()
        self.state_manager.set_state({"current_session": self.current_session})
        self.load_page()

    def end_session(self):
        self.current_session.end_session()
        self.state_manager.set_state({"current_session": self.current_session})
        self.load_page()

    def add_session(self, option_selected:str):
        subject_id = self.__get_subject_id(option_selected)
        if subject_id:
            self.current_session.subject_id = subject_id
            req = self.current_session.add_session()
            if req["successful"]:
                CTkMessagebox(
                    title="Session Added", 
                    message=f"Duration: {self.current_session.duration_mins} minutes",
                    icon="check"
                )
                user_sessions = self.state_manager.get_state()["user_sessions"]
                user_sessions.append(self.current_session)
                self.current_session = StudySession()
                self.state_manager.set_state(
                    {"user_sessions": user_sessions, "current_session": self.current_session}
                )
                self.load_page()
            else:
                CTkMessagebox(
                    title="Error Adding Session", 
                    message=req["message"],
                    icon="cancel"
                )
        else:
            CTkMessagebox(
                    title="No Subject Selected", 
                    message="Please select a subject",
                    icon="info"
                )
    
    def __get_subject_id(self, option):
        match = re.search(r"\((\d+)\)$", option)
        if match:
            return int(match.group(1))
        else:
            return None
        