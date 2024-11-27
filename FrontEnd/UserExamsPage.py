from customtkinter import CTkScrollableFrame, CTkFrame, CTkToplevel, CTkLabel, CTkEntry, CTkComboBox, CTkButton
from CTkMessagebox import CTkMessagebox
from datetime import datetime, date
import re
from Components.DatePicker import DatePicker
from DB.Queries.user_exam import UserExam
from DB.Queries.user_subject import UserSubject

class ExamsPage(CTkScrollableFrame):
  def __init__(self, master, state_manager):
    super().__init__(master)
    self.state_manager = state_manager
    self.subjects_to_id = self.fetch_user_subject_to_id()
    self.user_exams = self.fetch_user_exams()
    # self.state_manager.set_state({"user_exams": self.user_exams})
    self.add_exam_form = None

    self.load_page()

  def fetch_user_subject_to_id(self):
    subject = UserSubject("")
    req = subject.get_subject_to_id()
    if req["successful"]:
        return req["subjects"]
    else:
        CTkMessagebox(title="Error fetching subjects", message=req["message"], icon="cancel")
        return {}
  
  def fetch_user_exams(self):
    exam = UserExam()
    req = exam.get_all_exams()
    if req["successful"]:
      return req["exams"]
    else:
      CTkMessagebox(title="Error fetching exams", message=req["message"], icon="cancel")
  
  def open_add_exam_form(self):
    if self.add_exam_form is None or not self.add_exam_form.winfo_exists():
      self.add_exam_form = AddExamForm(master=self, subjects_to_id=self.subjects_to_id)
    else:
      self.add_exam_form.focus()
  
  def load_page(self):
    for row, e in enumerate(self.user_exams):
      ExamCard(self, e, self.subjects_to_id).pack()
    CTkButton(self, text="Add exam", command=self.open_add_exam_form).pack()

class ExamsContainer(CTkFrame):
  def __init__(self, master, subjects_to_id):
    super().__init__(master)
    self.subjects_to_id = subjects_to_id
    self.cards = []

class ExamCard(CTkFrame):
  def __init__(self, master, exam, subjects_to_id):
    super().__init__(master)
    self.exam = exam
    self.subjects_to_id = subjects_to_id

    self.configure(fg_color="#f5f5f5", corner_radius=10, border_width=1, border_color="#d3d3d3")

    self.title_label = CTkLabel(self, anchor="w", font=("Arial", 16, "bold"))
    self.subject_label = CTkLabel(self, anchor="w")
    self.exam_date_label = CTkLabel(self, anchor="w")
    self.remaining_days_label = CTkLabel(self, anchor="w")
  
    self.__load_card()

  def __load_card(self):
    self.__load_data()
    self.__place_widgets()

  def __place_widgets(self):
    self.title_label.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
    self.subject_label.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
    self.exam_date_label.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
    self.remaining_days_label.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
  
  def __load_data(self):
    subject = self.subjects_to_id.get(self.exam.subject_id, "Unknown")
    exam_date = self.__get_formatted_date()
    remaining_days = self.__get_remaining_days()
    self.title_label.configure(text=self.exam.title)
    self.subject_label.configure(text=f"Subject: {subject}")
    self.exam_date_label.configure(text=f"Exam date: {exam_date}")
    self.remaining_days_label.configure(text=f"Remaining days: {remaining_days}")
  
  def __get_formatted_date(self):
    """Returns the date in dd/mm/yyyy format as a string."""
    if isinstance(self.exam.exam_date, str):
        try:
            return datetime.strptime(self.exam.exam_date, "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError as e:
            raise ValueError(str(e))
    elif isinstance(self.exam.exam_date, date):
        return self.exam.exam_date.strftime("%d/%m/%Y")
    else:
        raise TypeError("Invalid due_date format")
  
  def __get_remaining_days(self):
    current_date = datetime.now().date()
    exam_date = datetime.strptime(self.__get_formatted_date(), "%d/%m/%Y").date()
    remaining_days = (exam_date - current_date).days
    return remaining_days


class AddExamForm(CTkToplevel):
  def __init__(self, master, subjects_to_id):
    super().__init__(master)
    self.title("Add exam")
    self.geometry("400x300")
    self.subjects_to_id = subjects_to_id

    self.subject_options = [
      f"{name}({id})" 
      for id, name in self.subjects_to_id.items()
    ]

    self.title_entry = CTkEntry(self, placeholder_text="title")
    self.subjects_selector = CTkComboBox(self, values=self.subject_options, state="readonly")
    self.date_picker = DatePicker(self)
    self.btn = CTkButton(self, text="Add", command=self.__add_exam)

    self.__create_form()
  def __create_form(self):
        self.title_entry.grid(row=0, column=0, sticky="ew", padx=10)

        self.subjects_selector.set("select subject")
        self.subjects_selector.grid(row=1, column=0, sticky="ew")

        self.date_picker.set_placeholder("Select due date")
        self.date_picker.grid(row=2, column=0, sticky="ew")

        self.btn.grid(row=3, column=0) 
  
  def __add_exam(self):
    title = self.title_entry.get()
    subject_id = self.__get_subject_id(self.subjects_selector.get())
    
    date_error = self.__check_date(self.date_picker.get_date())
    if date_error:
      CTkMessagebox(self, title="Incorrect Date Format", message=date_error, icon="info")
      return

    due_date = datetime.strptime(self.date_picker.get_date(), self.date_picker.date_format).date()
    
    if not subject_id:
      CTkMessagebox(title="Subject missing", message="Select a subject for the exam", icon="info")
      return
    
    exam = UserExam(title=title, exam_date=due_date, subject_id=subject_id)
    req = exam.add_exam()
    if req["successful"]:
      print("Exam added")
    else:
      print(req["message"])


  def __check_date(self,date):
        error = None
        try:
            parsed_date = datetime.strptime(date, "%d/%m/%Y")
            return None
        except ValueError:
            return "Date must be in the format yyyy-mm-dd" 
  
  def __get_subject_id(self, option):
    match = re.search(r"\((\d+)\)$", option)
    if match:
      return int(match.group(1))
    else:
      return None

  def close_form(self):
        self.after(300, self.destroy)
    