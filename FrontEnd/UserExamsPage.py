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
    self.state_manager.set_state({"user_exams": self.user_exams})
    self.add_exam_form = None
    self.exams_container = ExamsContainer(self, self.user_exams, self.subjects_to_id, on_remove_card=self.remove_exam)
    self.load_page()

    self.state_manager.subscribe(self.update_subjects_to_id, ["user_subjects"], self)

  def update_subjects_to_id(self, state):
    self.subjects_to_id = self.fetch_user_subject_to_id()

  def fetch_user_subject_to_id(self):
    subjects_to_id = {}
    subjects = self.state_manager.get_state()["user_subjects"]
    for s in subjects:
      subjects_to_id[s.id] = s.subject_name
    return subjects_to_id
  
  def fetch_user_exams(self):
    exam = UserExam()
    req = exam.get_all_exams()
    if req["successful"]:
      return req["exams"]
    else:
      CTkMessagebox(title="Error fetching exams", message=req["message"], icon="cancel")
  
  def open_add_exam_form(self):
    if self.add_exam_form is None or not self.add_exam_form.winfo_exists():
      self.add_exam_form = AddExamForm(master=self, subjects_to_id=self.subjects_to_id, on_add=self.add_exam)
    else:
      self.add_exam_form.focus()
  
  def add_exam(self, exam):
    current_exams = self.state_manager.get_state()["user_exams"]
    current_exams.append(exam)
    self.state_manager.set_state({"user_exam": current_exams})
    self.exams_container.add_card(exam=exam)
  
  
  def remove_exam(self, exam):
    req = exam.remove_exam()
    if req["successful"]:
      user_exams = self.state_manager.get_state()["user_exams"]
      user_exams = [e for e in user_exams if e.id != exam.id]
      self.state_manager.set_state({"user_exams": user_exams})
    else:
      CTkMessagebox(title="error deleting exam", message=req["message"], icon="cancel")
  
  def load_page(self):
    self.exams_container.grid(row=0, column=0, sticky="nsew")
    CTkButton(self, text="Add exam", command=self.open_add_exam_form).grid(row=1, column=0)

class ExamsContainer(CTkFrame):
  def __init__(self, master, user_exam, subjects_to_id, on_remove_card):
    super().__init__(master)
    self.user_exam = user_exam
    self.on_remove_card = on_remove_card
    self.subjects_to_id = subjects_to_id
    self.exams_cards = [] #tuple of (exam, card)

    self.columnconfigure([0, 1, 2, 3], weight=1) 
  
    for e in self.user_exam:
      self.add_card(exam=e)

  def add_card(self, exam):
    row = len(self.exams_cards)
    card = ExamCard(self, exam=exam, subjects_to_id=self.subjects_to_id, on_remove=self.__remove_card)
    row, col = divmod(len(self.exams_cards), 4) 
    card.grid(row=row, column=col, sticky="nsew", padx=10, pady=5)
    self.exams_cards.append((exam, card))
  
  def __remove_card(self, exam):
    confirm_options = ["No", "Yes delete"]
    confirmation = CTkMessagebox(
        title="Delete Exam?",
        message=f"Are you sure you want to delete the exam?",
        icon="question",
        options=confirm_options
    )
    if confirmation.get() == confirm_options[1]:
      for idx, (e, card) in enumerate(self.exams_cards):
        if e.id == exam.id:
          card.destroy()
          self.exams_cards.pop(idx)
          break
      self.on_remove_card(exam)
      self.__rearrange_cards()
  
  def __rearrange_cards(self):
    for idx, (e, card) in enumerate(self.exams_cards):
      row, col = divmod(idx, 4)
      card.grid(row=row, column=col, sticky="nsew", padx=10, pady=5)

class ExamCard(CTkFrame):
  def __init__(self, master, exam, subjects_to_id, on_remove):
    super().__init__(master)
    self.exam = exam
    self.subjects_to_id = subjects_to_id
    self.on_remove = on_remove

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
    
    CTkButton(
      self,
      text="Remove",
      fg_color="red",
      hover_color="#ff4d4d",
      command=lambda: self.on_remove(self.exam)
    ).grid(row=4, column=0, sticky="ew", padx=10, pady=5)

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
    if remaining_days < 0:
      return 0
    return remaining_days


class AddExamForm(CTkToplevel):
  def __init__(self, master, subjects_to_id, on_add):
    super().__init__(master)
    self.title("Add exam")
    self.geometry("400x300")
    self.subjects_to_id = subjects_to_id
    self.on_add = on_add

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
      self.on_add(exam)
      CTkMessagebox( 
        title="Exam Added", 
        message=f"Your exam date for {exam.title} is {self.date_picker.get_date()}", 
        icon="check"
        )
      self.__close_form()
    else:
      CTkMessagebox(title="Error adding exam", message=req["message"], icon="cancel")


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

  def __close_form(self):
        self.after(300, self.destroy)
    