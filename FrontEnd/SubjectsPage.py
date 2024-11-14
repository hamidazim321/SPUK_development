import tkinter as tk
from tkinter import Frame
from tkinter import font
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB.Queries.user_subject import UserSubject

class SubjectsPage(Frame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        
        # Fetch subjects initially and set state
        user_subjects = self.fetch_user_subjects()
        self.state_manager.set_state({"user_subjects": user_subjects})
        
        # get updated state
        self.state = None

        self.load_page()

    def fetch_user_subjects(self):
        # Fetch user subjects from DB and return the list
        subject = UserSubject("")
        req = subject.get_all_subjects()
        if req["successful"]:
            print("subjects fetched")
            return req["subjects"]
        else:
            messagebox.showerror("Error loading subjects", req["message"])
            return []

    def load_page(self):
        # Load static page with table
        for widget in self.winfo_children():
            widget.destroy()
        
        self.state = self.state_manager.get_state() 

        subframe = tk.Frame(self)
        subframe.pack(expand=True, fill="both")

        subjects_table = self.create_subjects_table(subframe)
        subjects_table.grid(row=0, column=0)

        add_subject_frame = tk.Frame(subframe)
        add_subject_frame.grid(row=1, column=0)

        add_subject_header = tk.Label(add_subject_frame, text="Add subject", font=font.Font(weight="bold"))
        add_subject_header.grid(row=0, column=0, columnspan=2)

        add_subject_name_label = tk.Label(add_subject_frame, text="subject name:")
        add_subject_name_entry = tk.Entry(add_subject_frame, fg='grey', bg='lightyellow', font=('Arial', 12), borderwidth=2, relief='groove')
        add_subject_name_label.grid(row=1, column=0)
        add_subject_name_entry.grid(row=1, column=1)

        add_current_chapter_label = tk.Label(add_subject_frame, text="current chapter: ")
        add_current_chapter_entry = tk.Entry(add_subject_frame, fg='grey', bg='lightyellow', font=('Arial', 12), borderwidth=2, relief='groove')
        add_current_chapter_label.grid(row=2, column=0)
        add_current_chapter_entry.grid(row=2, column=1)

        add_total_chapters_label = tk.Label(add_subject_frame, text="total chapters: ")
        add_total_chapters_entry = tk.Entry(add_subject_frame, fg='grey', bg='lightyellow', font=('Arial', 12), borderwidth=2, relief='groove')
        add_total_chapters_label.grid(row=3, column=0)
        add_total_chapters_entry.grid(row=3, column=1)

        add_subject_btn = tk.Button(
            add_subject_frame, 
            text="Add", 
            command=lambda:self.add_subject(
                add_subject_name_entry, 
                add_total_chapters_entry, 
                add_current_chapter_entry, 
                )
            )
        add_subject_btn.grid(row=4, column=0)

    def add_subject(self, name_entry, total_chapters_entry, current_chapter_entry):
        # Add subject to database and update local state
        name = name_entry.get()
        total_chapters = int(total_chapters_entry.get())
        current_chapter = int(current_chapter_entry.get())

        subject = UserSubject(name, current_chapter=current_chapter, total_chapters=total_chapters)
        try:
            req = subject.add_subject()
            if req["successful"]:
                self.state["user_subjects"].append(subject)
                self.load_page()
                print("subject added")
            else:
                messagebox.showerror("Error Adding Subject", req["message"])
        except Exception as e:
            print("Error Adding Subject", str(e))

    def create_subjects_table(self, master):
        # Create a subjects table from state
        table = tk.Frame(master, bd=2, relief="groove")
        table.pack(padx=10, pady=10)

        header_font = font.Font(weight="bold")

        headers = ["Subject Name", "Total Chapters", "Current Chapter", "Studied Mins", 'Remove Subject']
        for col, header in enumerate(headers):
            tk.Label(table, text=header, font=header_font, bg="#f0f0f0", padx=5, pady=5).grid(row=0, column=col, sticky="ew")
        
        subjects = self.state["user_subjects"]
        if len(subjects) > 0:
            for row, subject in enumerate(subjects, start=1):
                bg_color = "#e9e9e9" if row % 2 == 0 else "#ffffff"  

                tk.Label(table, text=subject.subject_name, bg=bg_color, padx=5, pady=5).grid(row=row, column=0, sticky="ew")
                tk.Label(table, text=subject.total_chapters, bg=bg_color, padx=5, pady=5).grid(row=row, column=1, sticky="ew")
                tk.Label(table, text=subject.current_chapter, bg=bg_color, padx=5, pady=5).grid(row=row, column=2, sticky="ew")
                tk.Label(table, text=subject.studied_mins, bg=bg_color, padx=5, pady=5).grid(row=row, column=3, sticky="ew")
                tk.Button(table, text="Remove", background="red", command=lambda:self.remove_subject(subject)).grid(row=row, column=4, sticky="ew")

        return table
    
    def remove_subject(self, subject:UserSubject):
        print(subject.subject_name)
        req = subject.remove_subject()
        if req["successful"]:
            current_subjects = self.state["user_subjects"]
            new_subjects = [subj for subj in current_subjects if subj.id != subject.id]
            self.state_manager.set_state({"user_subjects": new_subjects})
            self.load_page()
        else:
            messagebox.showerror("Error removing page", req["message"])
    

