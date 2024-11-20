from customtkinter import CTkScrollableFrame, CTkFrame, CTkToplevel, CTkLabel, CTkEntry, CTkButton
from CTkMessagebox import CTkMessagebox
from DB.Queries.user_subject import UserSubject


class SubjectsPage(CTkScrollableFrame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        self.user_subjects = self.fetch_user_subjects()
        self.state_manager.set_state({"user_subjects": self.user_subjects})
        self.state = self.state_manager.get_state()
        self.subjects_container = None
        self.add_subject_form = None
        self.load_page()

    def fetch_user_subjects(self):
        subject = UserSubject("")
        req = subject.get_all_subjects()
        if req["successful"]:
            return req["subjects"]
        else:
            CTkMessagebox(title="Error Loading Subjects", message=req["message"], icon="cancel")
            return []

    def load_page(self):
        subframe = CTkFrame(self)
        subframe.pack(expand=True, fill="both", padx=20, pady=20)

        # Subjects Table
        self.subjects_container = SubjectsContainer(subframe, self.state["user_subjects"], self.remove_subject, self.update_subject)
        self.subjects_container.grid(row=0, column=0, pady=10, sticky="nsew")

        # Add Subject Form
        add_subject_btn = CTkButton(subframe, text="Add subject", command=self.open_add_subject_form)
        add_subject_btn.grid(row=1, column=0)

    def open_add_subject_form(self):
        if self.add_subject_form is None or not self.add_subject_form.winfo_exists():
            self.add_subject_form = AddSubjectForm(self, self.add_subject)
        else:
            self.add_subject_form.focus()
    
    def update_subject(self, subject):
        old_name = ""
        user_subjects = self.state_manager.get_state()["user_subjects"]
        for idx, subj in enumerate(user_subjects):
            if subj.id == subject.id:
                old_name = subj.subject_name
                user_subjects[idx] = subject
                self.state_manager.set_state({"user_subjects": user_subjects})
                CTkMessagebox(title="Subject Updated", message="subject updated")
    
    def add_subject(self, subject):
        self.user_subjects.append(subject)
        self.state_manager.set_state({"user_subjects": self.user_subjects})
        self.subjects_container.add_card(subject)
        CTkMessagebox(title="Subject Added", message=f"{subject.subject_name} Added", icon="check")
        
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
                self.subjects_container.remove_card(subject.id)
                self.user_subjects = [subj for subj in self.user_subjects if subj.id != subject.id]
                self.state_manager.set_state({"user_subjects": self.user_subjects})
                CTkMessagebox(title="Subject Removed", message=f"{subject.subject_name} removed successfully!", icon="check")
            else:
                CTkMessagebox(title="Error Removing Subject", message=req["message"], icon="cancel")

# Dynamic components
class SubjectsContainer(CTkFrame):
    def __init__(self, master, subjects, on_remove_subject, on_update_subject):
        super().__init__(master)
        self.on_remove_subject = on_remove_subject
        self.on_update_subject = on_update_subject
        self.cards = []
        
        self.columnconfigure([0, 1, 2], weight=1) 

        for subject in subjects:
            self.add_card(subject)

    def add_card(self, subject):
        card = SubjectCard(self, subject, self.on_remove_subject, self.on_update_subject)
        row, col = divmod(len(self.cards), 3) 
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        self.cards.append(card)

    def remove_card(self, subject_id):
        for card in self.cards:
            if card.subject.id == subject_id:
                card.destroy()
                self.cards.remove(card)
                self.rearrange_cards()
                break

    def rearrange_cards(self):
        for idx, card in enumerate(self.cards):
            row, col = divmod(idx, 3)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")


class SubjectCard(CTkFrame):
    def __init__(self, master, subject, on_remove, on_update):
        super().__init__(master)
        self.subject = subject
        self.on_remove = on_remove
        self.on_update = on_update
        self.update_subject_form = None

        self.configure(fg_color="#f5f5f5", corner_radius=10, border_width=1, border_color="#d3d3d3")
        
        # Subject details
        self.name_label = CTkLabel(self, text=f"{subject.subject_name}", anchor="w", font=("Arial", 24, "bold"))
        self.name_label.grid(row=0, column=0, sticky="ew", padx=5, pady=2)
        self.chapters_label = CTkLabel(self, text=f"Chapters: {subject.total_chapters}", anchor="w")
        self.chapters_label.grid(row=1, column=0, sticky="ew", padx=5, pady=2)
        self.current_chapter_label = CTkLabel(self, text=f"Current: {subject.current_chapter}", anchor="w")
        self.current_chapter_label.grid(row=2, column=0, sticky="ew", padx=5, pady=2)
        CTkLabel(self, text=f"Minutes: {subject.studied_mins}", anchor="w").grid(row=3, column=0, sticky="ew", padx=5, pady=2)
        
        # Remove and update button
        btns_frame = CTkFrame(self)
        btns_frame.grid(row=4, column=0, pady=(5, 0), sticky="ew")

        CTkButton(
            btns_frame,
            text="Update",
            fg_color = "#348feb",
            hover_color= "#3480eb",
            command=self.open_update_subject_form
        ).grid(row=0, column=0)

        CTkButton(
            btns_frame,
            text="Remove",
            fg_color="red",
            hover_color="#ff4d4d",
            command=lambda: self.on_remove(self.subject)
        ).grid(row=0, column=1)


        
        self.rowconfigure([0, 1, 2, 3, 4], weight=1)
        self.columnconfigure([0], weight=1)

    def open_update_subject_form(self):
        if self.update_subject_form is None or not self.update_subject_form.winfo_exists():
            self.update_subject_form = UpdateSubjectForm(self, self.subject, self.update_card)
        else:
            self.update_subject_form.focus()
            
    def update_card(self, subject):
        self.name_label.configure(text=subject.subject_name)
        self.chapters_label.configure(text=f"Chapters: {subject.total_chapters}")
        self.current_chapter_label.configure(text=f"Current: {subject.current_chapter}")
        self.on_update(subject)

class AddSubjectForm(CTkToplevel):
    def __init__(self, master, on_add):
        super().__init__(master)
        self.title("Add a subject")
        self.geometry("400x300")
        self.on_add = on_add

        self.create_form()

    def create_form(self):
        add_subject_frame = CTkFrame(self)
        add_subject_frame.pack(expand=True, fill="both")

        CTkLabel(add_subject_frame, text="Add Subject").grid(row=0, column=0, columnspan=2, pady=(0, 10))
        # Inputs
        subject_name_entry = CTkEntry(add_subject_frame, placeholder_text="subject name")
        subject_name_entry.grid(row=1, column=0, pady=5, sticky="ew")

        current_chapter_entry = CTkEntry(add_subject_frame, placeholder_text="current_chapter")
        current_chapter_entry.grid(row=2, column=0, pady=5, sticky="ew")

        total_chapters_entry = CTkEntry(add_subject_frame, placeholder_text="total chapters")
        total_chapters_entry.grid(row=3, column=0, pady=5, sticky="ew")

        CTkButton(
            add_subject_frame,
            text="Add Subject",
            command=lambda: self.__add_subject(name_entry=subject_name_entry, total_chapters_entry=total_chapters_entry, current_chapter_entry=current_chapter_entry)
        ).grid(row=4, column=0, columnspan=2, pady=10)
    
    def __add_subject(self, name_entry, total_chapters_entry, current_chapter_entry):
        try:
            name = name_entry.get()
            total_chapters = total_chapters_entry.get()
            current_chapter = current_chapter_entry.get()
            error = SubjectInputValidation.check_subject_input(name, current_chapter, total_chapters)
            if error:
                CTkMessagebox(title="Incorrect Input", message=error, icon="info")
                return
            subject = UserSubject(name, current_chapter=current_chapter, total_chapters=total_chapters)
            req = subject.add_subject()
            if req["successful"]:
                self.on_add(subject)
                self.__close_form()
            else:
                CTkMessagebox(title="Error Adding Subject", message=req["message"], icon="cancel")
        except ValueError:
            CTkMessagebox(title="Invalid Input", message="Invalid input values.", icon="info")
    
    def __close_form(self):
        self.after(300, self.destroy)
    
class UpdateSubjectForm(CTkToplevel):
    def __init__(self, master, subject, on_update):
        super().__init__(master)
        self.geometry("400x300")
        self.on_update = on_update
        self.subject = subject
        self.create_update_subject_form()

    def create_update_subject_form(self):
        self.title("Update Subject")
        update_subject_frame = CTkFrame(self)
        update_subject_frame.pack(expand=True, fill="both")

        CTkLabel(update_subject_frame, text="Update Subject").grid(row=0, column=0, columnspan=2, pady=(0, 10))
        # Inputs
        subject_name_entry = CTkEntry(update_subject_frame, placeholder_text="subject name")
        subject_name_entry.insert(0, self.subject.subject_name)  
        subject_name_entry.grid(row=1, column=0, pady=5, sticky="ew")

        current_chapter_entry = CTkEntry(update_subject_frame, placeholder_text="current_chapter")
        current_chapter_entry.insert(0, self.subject.current_chapter)
        current_chapter_entry.grid(row=2, column=0, pady=5, sticky="ew")

        total_chapters_entry = CTkEntry(update_subject_frame, placeholder_text="total chapters")
        total_chapters_entry.insert(0, self.subject.total_chapters)
        total_chapters_entry.grid(row=3, column=0, pady=5, sticky="ew")

        CTkButton(
            update_subject_frame,
            text="Update Subject",
            command=lambda: self.__update_subject(subject=self.subject, name_entry=subject_name_entry, total_chapters_entry=total_chapters_entry, current_chapter_entry=current_chapter_entry)
        ).grid(row=4, column=0, columnspan=2, pady=10)
    
    def __update_subject(self, subject:UserSubject, name_entry, total_chapters_entry, current_chapter_entry):
        name = name_entry.get()
        total_chapters = total_chapters_entry.get()
        current_chapter = current_chapter_entry.get()
        error = SubjectInputValidation.check_subject_input(name, current_chapter, total_chapters)
        if error:
            CTkMessagebox(title="Incorrect Input", message=error, icon="info")
            return
        subject.subject_name = name
        subject.current_chapter = current_chapter
        subject.total_chapters = total_chapters
        try:
            req = subject.update_subject()
            if req["successful"]:
                self.on_update(subject)
                self.__close_form()
            else:
                CTkMessagebox(title="Error updating subject", message=req["message"], icon="cancel")
        except Exception as e:
            print("An Exception occured when clicking update subject button from form:",e)
            CTkMessagebox(title="An Exception occured", message=str(e), icon="cancel")
    
    def __close_form(self):
        self.after(300, self.destroy)

# Input Validation
class SubjectInputValidation:
    @staticmethod
    def __check_current_total_chapters(current_chapter, total_chapters):
        try:
            current_chapter = int(current_chapter)
            total_chapters = int(total_chapters)
        except ValueError:
            return "current chapter and total chapters must be valid integers"
        
        if not current_chapter or not total_chapters:
            return "current chapter and total chapters must be entered"
        elif current_chapter > total_chapters:
            return "current chapter must be smaller than total chapters"
        else:
            return None
    
    @staticmethod
    def __check_subject_name(name):
        if not name:
            return "subject name must be entered"
        else:
            return None
    
    @staticmethod
    def check_subject_input(name, current_chapter, total_chapters):
        error = SubjectInputValidation.__check_subject_name(name)
        if error:
            return error
        error = SubjectInputValidation.__check_current_total_chapters(current_chapter, total_chapters)
        if error:
            return error
        else:
            return None
