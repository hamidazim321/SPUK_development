import re
import datetime
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkComboBox
from CTkMessagebox import CTkMessagebox
from DB.Queries.user_subject import UserSubject
from DB.Queries.study_session import StudySession


class StartSessionPage(CTkFrame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.initial_load = False
        self.state_manager = state_manager
        self.state = self.state_manager.get_state()
        self.set_global_session()
        self.user_subjects = self.state["user_subjects"].copy()
        self.subject_options = [f"{subject.subject_name}({subject.id})" for subject in self.user_subjects]
        self.current_session = self.state["current_session"]
        self.state_manager.subscribe(self.update_page, ["user_subjects"], self)

        self.subjects_selector = None
        self.session_btn = None
        self.timer = None

        self.load_page()

    
    def destroy(self):
        self.state_manager.unsubscribe(self)
        super().destroy()

    def set_global_session(self):
        if self.state["current_session"] is None:
            session = StudySession()
            self.state_manager.set_state({"current_session": session})
            self.state["current_session"] = session

    def update_page(self, state):
        self.state = state
        self.user_subjects = self.state["user_subjects"]
        self.subject_options = [f"{subject.subject_name}({subject.id})" for subject in self.user_subjects]
        if self.subjects_selector:
            self.subjects_selector.configure(values=self.subject_options)

    def load_page(self):
        print("session page loaded")
        subframe = CTkFrame(self)
        subframe.pack(expand=True, fill="both", padx=20, pady=20)

        # Subject selector dropdown
        self.subjects_selector = CTkComboBox(
            subframe,
            values=self.subject_options,
            state="readonly",
        )
        self.subjects_selector.set("Select subject")
        self.subjects_selector.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

        # Start Session button
        self.session_btn = CTkButton(
            subframe,
            fg_color = "#348feb",
            hover_color= "#3480eb",
            text="Start Session",
            command=self.start_session,
        )
        self.session_btn.grid(row=2, column=0, padx=10, pady=10, sticky="ew")


        # Timer display
        timer_frame = CTkFrame(subframe)
        timer_frame.grid(row=3, column=0, columnspan=2, pady=10)
        self.timer = Timer(timer_frame)
        self.timer.pack()

    def start_session(self):
        self.current_session.start_session()
        self.timer.start_timer()
        self.state_manager.set_state({"current_session": self.current_session})
        self.session_btn.configure(
            text="End Session",
            fg_color="red",
            hover_color="#ff4d4d",
            command=self.end_session,
        )

    def end_session(self):
        self.current_session.end_session()
        self.timer.stop_timer()
        self.state_manager.set_state({"current_session": self.current_session})
        self.session_btn.configure(
            text="Add Session",
            fg_color="green",
            hover_color="#33cc33",
            command=lambda: self.add_session(self.subjects_selector.get()),
        )

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
                self.timer.reset_timer()

                user_sessions = self.state_manager.get_state()["user_sessions"]
                user_sessions.append(self.current_session)
                self.current_session = StudySession()
                self.state_manager.set_state(
                    {"user_sessions": user_sessions, "current_session": self.current_session}
                )
                self.session_btn.configure(
                    fg_color = "#348feb",
                    hover_color= "#3480eb",
                    text="Start Session",
                    command=self.start_session,
                )
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

# Dynamic components
class Timer(CTkLabel):
    def __init__(self, master):
        super().__init__(master, font=("Arial", 12, "bold"), text_color="white")
        self.start_time = None
        self.__update_id = None  
        self.configure(text="00:00")
    
    def start_timer(self):
        self.start_time = datetime.datetime.now() 
        self.__update_timer()

    def stop_timer(self):
        if self.__update_id:
            self.after_cancel(self.__update_id)

    def reset_timer(self):
        self.configure(text="00:00")  

    def __calculate_time(self):
        elapsed_time = 0
        if self.start_time:
            elapsed_time = (datetime.datetime.now() - self.start_time).total_seconds()

        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        return f"{minutes:02}:{seconds:02}"

    def __update_timer(self):
        self.configure(text=self.__calculate_time())
        self.__update_id = self.after(1000, self.__update_timer)


