from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from CTkMessagebox import CTkMessagebox
from DB.Queries.user_subject import UserSubject


class SubjectsPage(CTkFrame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        self.initial_load = False
        self.user_subjects = self.fetch_user_subjects()
        self.state_manager.set_state({"user_subjects": self.user_subjects})
        self.state = self.state_manager.get_state()
        self.subjects_table = None
        self.load_page()

    def fetch_user_subjects(self):
        subject = UserSubject("")
        req = subject.get_all_subjects()
        if req["successful"]:
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
        self.subjects_table = SubjectsTable(subframe, self.state["user_subjects"], self.remove_subject)
        self.subjects_table.grid(row=0, column=0, pady=10)

        # Add Subject Form
        self.create_add_subject_form(subframe)

    def create_add_subject_form(self, master):
        add_subject_frame = CTkFrame(master)
        add_subject_frame.grid(row=1, column=0, pady=10)

        CTkLabel(add_subject_frame, text="Add Subject").grid(row=0, column=0, columnspan=2, pady=(0, 10))
        # Inputs
        CTkLabel(add_subject_frame, text="Subject Name:").grid(row=1, column=0, pady=5, sticky="e")
        subject_name_entry = CTkEntry(add_subject_frame)
        subject_name_entry.grid(row=1, column=1, pady=5, sticky="w")

        CTkLabel(add_subject_frame, text="Current Chapter:").grid(row=2, column=0, pady=5, sticky="e")
        current_chapter_entry = CTkEntry(add_subject_frame)
        current_chapter_entry.grid(row=2, column=1, pady=5, sticky="w")

        CTkLabel(add_subject_frame, text="Total Chapters:").grid(row=3, column=0, pady=5, sticky="e")
        total_chapters_entry = CTkEntry(add_subject_frame)
        total_chapters_entry.grid(row=3, column=1, pady=5, sticky="w")

        CTkButton(
            add_subject_frame,
            text="Add Subject",
            command=lambda: self.add_subject(subject_name_entry, total_chapters_entry, current_chapter_entry)
        ).grid(row=4, column=0, columnspan=2, pady=10)

    def add_subject(self, name_entry, total_chapters_entry, current_chapter_entry):
        try:
            name = name_entry.get()
            total_chapters = int(total_chapters_entry.get())
            current_chapter = int(current_chapter_entry.get())

            subject = UserSubject(name, current_chapter=current_chapter, total_chapters=total_chapters)
            req = subject.add_subject()
            if req["successful"]:
                print("AD:Initial Len:", len(self.state_manager.get_state()["user_subjects"]))
                self.subjects_table.add_row(subject)
                self.user_subjects.append(subject)
                self.state_manager.set_state({"user_subjects": self.user_subjects })
                print("AD:New Len:", len(self.state_manager.get_state()["user_subjects"]))
                CTkMessagebox(title="Subject Added", message=f"{name} Added", icon="check")
            else:
                CTkMessagebox(title="Error Adding Subject", message=req["message"], icon="cancel")
        except ValueError:
            CTkMessagebox(title="Invalid Input", message="Invalid input values.", icon="info")

    def remove_subject(self, subject):
        confirm_options = ["No", "Yes delete"]
        confirmation = CTkMessagebox(
            title="Delete Subject?",
            message=f"Are you sure you want to delete {subject.subject_name}?",
            icon="question",
            options=confirm_options
        )
        if confirmation.get() == confirm_options[1]:
            req = subject.remove_subject()
            if req["successful"]:
                print("RM:Initial Len:", len(self.state_manager.get_state()["user_subjects"]))
                self.subjects_table.remove_row(subject.id)
                self.user_subjects = [subj for subj in self.user_subjects if subj.id != subject.id]
                self.state_manager.set_state({"user_subjects": self.user_subjects})
                print("RM:New Len:", len(self.state_manager.get_state()["user_subjects"]))
                CTkMessagebox(title="Subject Removed", message=f"{subject.subject_name} removed successfully!", icon="check")
            else:
                CTkMessagebox(title="Error Removing Subject", message=req["message"], icon="cancel")
        
# Dynamic components
class SubjectsTable(CTkFrame):
    def __init__(self, master, subjects, on_remove_subject):
        super().__init__(master)
        self.on_remove_subject = on_remove_subject
        self.rows = []
        
        # Create headers
        headers = ["Subject Name", "Total Chapters", "Current Chapter", "Studied Mins", "Remove"]
        for col, header in enumerate(headers):
            CTkLabel(self, text=header, padx=5, pady=5).grid(row=0, column=col, sticky="ew")

        # Add initial rows
        for subject in subjects:
            self.add_row(subject)
    
    def add_row(self, subject):
        row = SubjectRow(self, subject, self.on_remove_subject)
        row.grid(row=len(self.rows) + 1, column=0, columnspan=5, sticky="ew")
        self.rows.append(row)

    def remove_row(self, subject_id):
        for row in self.rows:
            if row.subject.id == subject_id:
                row.destroy()
                self.rows.remove(row)
                break

class SubjectRow(CTkFrame):
    def __init__(self, master, subject, on_remove):
        super().__init__(master)
        self.subject = subject
        self.on_remove = on_remove
        
        bg_color = "#e9e9e9" if (subject.id % 2 == 0) else "#ffffff"
        
        CTkLabel(self, text=subject.subject_name, fg_color=bg_color, padx=5, pady=5).grid(row=0, column=0, sticky="ew")
        CTkLabel(self, text=subject.total_chapters, fg_color=bg_color, padx=5, pady=5).grid(row=0, column=1, sticky="ew")
        CTkLabel(self, text=subject.current_chapter, fg_color=bg_color, padx=5, pady=5).grid(row=0, column=2, sticky="ew")
        CTkLabel(self, text=subject.studied_mins, fg_color=bg_color, padx=5, pady=5).grid(row=0, column=3, sticky="ew")
        
        CTkButton(
            self,
            text="Remove",
            fg_color="red",
            hover_color="#ff4d4d",
            command=lambda: self.on_remove(self.subject)
        ).grid(row=0, column=4, sticky="ew")
