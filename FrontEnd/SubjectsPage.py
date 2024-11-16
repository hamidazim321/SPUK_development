from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from CTkMessagebox import CTkMessagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB.Queries.user_subject import UserSubject


class SubjectsPage(CTkFrame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        self.initial_load = False
        # Fetch subjects initially and set state
        user_subjects = self.fetch_user_subjects()
        self.state_manager.set_state({"user_subjects": user_subjects})
        
        # Get updated state
        self.state = self.state_manager.get_state()
        self.state_manager.subscribe(self.update_page)
    
    def update_page(self, state):
        if not self.initial_load:
            self.load_page()
            self.initial_load = True
        elif len(self.state["user_subjects"]) != len(state["user_subjects"]):
            self.state = state
            self.load_page()

    def fetch_user_subjects(self):
        subject = UserSubject("")
        req = subject.get_all_subjects()
        if req["successful"]:
            print("Subjects fetched")
            return req["subjects"]
        else:
            CTkMessagebox.show_error("Error Loading Subjects", req["message"])
            return []

    def load_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        subframe = CTkFrame(self)
        subframe.pack(expand=True, fill="both", padx=20, pady=20)

        # Subjects Table
        subjects_table = self.create_subjects_table(subframe)
        subjects_table.grid(row=0, column=0, pady=10)

        # Add Subject Form
        add_subject_frame = CTkFrame(subframe)
        add_subject_frame.grid(row=1, column=0, pady=10)

        CTkLabel(add_subject_frame, text="Add Subject",).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Subject Name Input
        CTkLabel(add_subject_frame, text="Subject Name:").grid(row=1, column=0, pady=5, sticky="e")
        subject_name_entry = CTkEntry(add_subject_frame)
        subject_name_entry.grid(row=1, column=1, pady=5, sticky="w")

        # Current Chapter Input
        CTkLabel(add_subject_frame, text="Current Chapter:").grid(row=2, column=0, pady=5, sticky="e")
        current_chapter_entry = CTkEntry(add_subject_frame)
        current_chapter_entry.grid(row=2, column=1, pady=5, sticky="w")

        # Total Chapters Input
        CTkLabel(add_subject_frame, text="Total Chapters:").grid(row=3, column=0, pady=5, sticky="e")
        total_chapters_entry = CTkEntry(add_subject_frame)
        total_chapters_entry.grid(row=3, column=1, pady=5, sticky="w")

        # Add Subject Button
        CTkButton(
            add_subject_frame,
            text="Add Subject",
            command=lambda: self.add_subject(
                subject_name_entry, total_chapters_entry, current_chapter_entry
            )
        ).grid(row=4, column=0, columnspan=2, pady=10)
    
    def create_subjects_table(self, master):
        table = CTkFrame(master)
        table.pack(padx=10, pady=10)

        headers = ["Subject Name", "Total Chapters", "Current Chapter", "Studied Mins", "Remove"]

        for col, header in enumerate(headers):
            CTkLabel(table, text=header, padx=5, pady=5).grid(row=0, column=col, sticky="ew")

        subjects = self.state["user_subjects"]
        for row, subject in enumerate(subjects, start=1):
            bg_color = "#e9e9e9" if row % 2 == 0 else "#ffffff"

            CTkLabel(table, text=subject.subject_name, fg_color=bg_color, padx=5, pady=5).grid(row=row, column=0, sticky="ew")
            CTkLabel(table, text=subject.total_chapters, fg_color=bg_color, padx=5, pady=5).grid(row=row, column=1, sticky="ew")
            CTkLabel(table, text=subject.current_chapter, fg_color=bg_color, padx=5, pady=5).grid(row=row, column=2, sticky="ew")
            CTkLabel(table, text=subject.studied_mins, fg_color=bg_color, padx=5, pady=5).grid(row=row, column=3, sticky="ew")

            CTkButton(
                table,
                text="Remove",
                fg_color="red",
                hover_color="#ff4d4d",
                command=lambda subj=subject: self.remove_subject(subj),
            ).grid(row=row, column=4, sticky="ew")

        return table

    def add_subject(self, name_entry, total_chapters_entry, current_chapter_entry):
        try:
            name = name_entry.get()
            total_chapters = int(total_chapters_entry.get())
            current_chapter = int(current_chapter_entry.get())

            subject = UserSubject(name, current_chapter=current_chapter, total_chapters=total_chapters)
            req = subject.add_subject()
            if req["successful"]:
                new_subjects = self.state["user_subjects"].copy()
                print("initial subjects length:", len(new_subjects))
                new_subjects.append(subject)
                print("New subjects length:", len(new_subjects))
                print("State subjects len:", len(self.state["user_subjects"]))
                self.state_manager.set_state({"user_subjects": new_subjects})
                CTkMessagebox(title="Subject Added", message=f"{name} Added", icon="check")
            else:
                CTkMessagebox(title="Error Adding Subject", message=req["message"], icon="cancel")

        except ValueError as e:
            CTkMessagebox(
                title="Invalid Input", 
                message=str(e), 
                icon="info")
        except Exception as e:
            CTkMessagebox(title="Error adding subject", message=str(e), icon="cancel")

    def remove_subject(self, subject: UserSubject):
        confirm_options = ["No", "Yes delete"]
        confirmation = CTkMessagebox(
            title="Delete Subject?",
            message=f"Are you sure you want to delete {subject.subject_name}?",
            icon="question",
            options=confirm_options
            )
        response = confirmation.get()
        if response == confirm_options[1]:
            req = subject.remove_subject()
            if req["successful"]:
                current_subjects = self.state["user_subjects"]
                new_subjects = [subj for subj in current_subjects if subj.id != subject.id]
                self.state_manager.set_state({"user_subjects": new_subjects})
                CTkMessagebox(
                    title="Subject Removed", 
                    message=f"{subject.subject_name} removed successfully!",
                    icon="check"
                    )
            else:
                CTkMessagebox(title="Error Removing Subject", message=req["message"], icon="cancel")
        

