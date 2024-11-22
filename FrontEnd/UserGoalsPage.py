from customtkinter import CTkScrollableFrame, CTkFrame, CTkToplevel, CTkLabel, CTkEntry, CTkButton, CTkTextbox
from CTkMessagebox import CTkMessagebox
from Components.DatePicker import DatePicker
from datetime import datetime, date
from DB.Queries.user_goal import UserGoal


class GoalsPage(CTkScrollableFrame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        self.user_goals = self.fetch_user_goals()
        self.state_manager.set_state({"user_goals": self.user_goals})

        self.goals_container = GoalsContainer(self, user_goals=self.user_goals, on_remove_goal=self.remove_goal)
        self.add_goal_form = None

        self.load_page()

    def fetch_user_goals(self):
        user_goal = UserGoal()
        req = user_goal.get_all_goals()
        if req["successful"]:
            return req["goals"]
        else:
            CTkMessagebox(title="Error fetching goals", message=req["message"], icon="cancel")
            return []

    def add_goal(self, goal:UserGoal):
        current_goals = self.state_manager.get_state()["user_goals"]
        current_goals.append(goal)
        self.state_manager.set_state({"user_goals": current_goals})
        self.goals_container.add_goal(goal)
        CTkMessagebox(title="Goal added", message=f"your due date is {goal.due_date}", icon="check")
    
    def remove_goal(self, goal:UserGoal):
        current_goals = self.state_manager.get_state()["user_goals"]
        for idx, g in enumerate(current_goals):
            if g.id == goal.id:
                current_goals.pop(idx)
                self.state_manager.set_state({"user_goals": current_goals})
                break

    def open_add_subject_form(self):
        if self.add_goal_form is None or not self.add_goal_form.winfo_exists():
            self.add_goal_form = AddGoalForm(self, self.add_goal)
        else:
            self.add_goal_form.focus()

    def load_page(self):
        self.goals_container.grid(row=0, column=0, sticky="nsew")
        CTkButton(self, text="Add goal", command=self.open_add_subject_form).grid(row=1, column=0)

class GoalsContainer(CTkFrame):
    def __init__(self, master, user_goals, on_remove_goal):
        super().__init__(master)
        self.on_remove_goal = on_remove_goal
        self.goals_cards = [] #tuple of (goal, card)

        for user_goal in user_goals:
            self.add_goal(user_goal)
    
    def add_goal(self, goal):
        row = len(self.goals_cards)
        card = GoalCard(self, goal=goal, on_remove_card=self.__remove_card)
        card.grid(row=row, column=0, sticky="nsew")
        self.goals_cards.append((goal, card))

    def __remove_card(self, goal:UserGoal):
        self.on_remove_goal(goal)
        for idx, (g, card) in enumerate(self.goals_cards):
            if g.id == goal.id: 
                self.goals_cards.pop(idx)
                break



class GoalCard(CTkFrame):
    def __init__(self, master, goal, on_remove_card):
        super().__init__(master)
        self.goal = goal
        self.on_remove_card = on_remove_card
        self.update_goal_form = None

        self.title_label = CTkLabel(self, anchor="w", font=("Arial", 16, "bold"))
        self.description_label = None
        self.due_date_label = None
        self.status_label = None
        self.achieve_btn = None

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)


        self.configure(border_width=5, corner_radius=10, fg_color="lightgray")
        self.grid(padx=10, pady=10) 

        self.__load_card()

    def __load_card(self):
        self.__create_card_widgets()
        self.__load_data()

    def __create_card_widgets(self):
        self.title_label = CTkLabel(self, anchor="w", font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        self.status_label = CTkLabel(self, anchor="e", justify="right", font=("Arial", 12, "bold"))
        self.status_label.grid(row=0, column=3, sticky="ew", padx=10, pady=5)

        self.description_label = CTkLabel(self, anchor="w", wraplength=300)
        self.description_label.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

        self.due_date_label = CTkLabel(self, anchor="w", font=("Arial", 12, "bold"))
        self.due_date_label.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        self.achieve_btn = CTkButton(
            self,
            command=self.__toggle_achieved
        )
        self.achieve_btn.grid(row=3, column=3, sticky="e", padx=10, pady=5)

        CTkButton(
            self,
            text="Update",
            command=self.__open_update_goal_form
        ).grid(row=3, column=0, padx=10, pady=5)

        CTkButton(
            self,
            text="Delete",
            fg_color="red",
            hover_color="#ff4d4d",
            command=self.__remove_card
        ).grid(row=3, column=1, padx=10, pady=5)

    def __load_data(self):
        self.title_label.configure(text=self.goal.title)
        self.description_label.configure(text=self.goal.description)
        self.due_date_label.configure(text=f"Due date: {self.__get_formatted_date()}")
        self.__set_card_status()

    def __set_card_status(self):
        goal_due_date = datetime.strptime(self.__get_formatted_date(), "%d/%m/%Y").date()
        current_date = datetime.today().date()
        if self.goal.achieved:
            self.configure(border_color="green")
            self.status_label.configure(text="achieved", text_color="green")
            self.achieve_btn.configure(text="unachieve", fg_color="#fca103", hover_color="#fc9403")
        elif goal_due_date > current_date:
            self.configure(border_color="blue")
            self.status_label.configure(text="upcoming", text_color="blue")
            self.achieve_btn.configure(text="achieve", fg_color="#a903fc", hover_color="#9003fc")
        else:
            self.configure(border_color="red")
            self.status_label.configure(text="overdue", text_color="red" )
            self.achieve_btn.configure(text="achieve", fg_color="#a903fc", hover_color="#9003fc")
    
    def __remove_card(self):
        confirmation_options = ["Yes", "No"]
        confirmation = CTkMessagebox(
            title="Confirm delete",
            message="Are you sure you want to delete this goal?",
            icon = "question",
            options= confirmation_options
            )
        response = confirmation.get()
        if response == confirmation_options[0]:
            self.on_remove_card(self.goal)
            self.goal.remove_goal()
            self.destroy()

    def __update_card(self):
        print("card updated")
        self.__load_card()

    def __toggle_achieved(self):
        self.goal.toggle_achieved()
        self.__set_card_status()

    def __get_formatted_date(self):
        """Returns the date in dd/mm/yyyy format as a string."""
        if isinstance(self.goal.due_date, str):
            try:
                return datetime.strptime(self.goal.due_date, "%Y-%m-%d").strftime("%d/%m/%Y")
            except ValueError as e:
                raise ValueError(str(e))
        elif isinstance(self.goal.due_date, date):
            return self.goal.due_date.strftime("%d/%m/%Y")
        else:
            raise TypeError("Invalid due_date format")

    def __open_update_goal_form(self):
        if self.update_goal_form is None or not self.update_goal_form.winfo_exists():
            self.update_goal_form = UpdateGoalForm(
                self, 
                goal=self.goal, 
                on_update=self.__update_card, 
                current_formatted_date=self.__get_formatted_date()
            )
        else:
            self.update_goal_form.focus()

class GoalForm(CTkToplevel):
    def __init__(self, master, btn_text):
        super().__init__(master)
        self.title("Goal Form")
        self.geometry("400x300")
        self.title_entry = CTkEntry(self, placeholder_text="title")
        self.description_box = CTkTextbox(self)
        self.date_picker = DatePicker(self)
        self.btn = CTkButton(self, text=btn_text, command=self.execute_form)

        self.__create_form()
    
    def __create_form(self):
        self.title_entry.grid(row=0, column=0, sticky="ew", padx=10)

        self.description_box.grid(row=1, column=0, sticky="ew")

        self.date_picker.set_placeholder("Select due date")
        self.date_picker.grid(row=2, column=0, sticky="ew")

        self.btn.grid(row=3, column=0) 
    
    def close_form(self):
        self.after(300, self.destroy)
    
    def check_date(self,date):
        error = None
        try:
            parsed_date = datetime.strptime(date, "%d/%m/%Y")
            return None
        except ValueError:
            return "Date must be in the format yyyy-mm-dd" 

    def execute_form(self):
        raise NotImplementedError("The __execute_form method is not implemented yet")

class AddGoalForm(GoalForm):
    def __init__(self, master, on_add):
        super().__init__(master, btn_text="Add Goal")
        self.title("Add a goal")
        self.geometry("400x300")
        self.on_add = on_add
    
    def execute_form(self):
        date_error = self.check_date(self.date_picker.get_date())
        if date_error:
            CTkMessagebox(title="Incorrect date format", message=date_error, icon="cancel")
            return
        title = self.title_entry.get()
        description = self.description_box.get("0.0", "end").strip()
        due_date = datetime.strptime(self.date_picker.get_date(), self.date_picker.date_format).date()

        goal = UserGoal(title=title, description=description, due_date=due_date)
        req = goal.add_goal()
        if req["successful"]:
            self.on_add(goal)
            self.close_form()
        else:
            CTkMessagebox("Error adding goal", message=req["message"], icon="cancel")
        return

class UpdateGoalForm(GoalForm):
    def __init__(self, master, goal:UserGoal, on_update, current_formatted_date:str):
        super().__init__(master, btn_text="Update Goal")
        self.title("Update goal")
        self.goal = goal
        self.on_update = on_update
        
        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, self.goal.title)

        self.description_box.delete("1.0", "end")
        self.description_box.insert("1.0", self.goal.description)

        self.date_picker.set_placeholder(current_formatted_date)
    def execute_form(self):
        date_error = self.check_date(self.date_picker.get_date())
        if date_error:
            CTkMessagebox(title="Incorrect date format", message=date_error, icon="cancel")
            return
        self.goal.title = self.title_entry.get()
        self.goal.description = self.description_box.get("0.0", "end").strip()
        self.goal.due_date = datetime.strptime(self.date_picker.get_date(), self.date_picker.date_format).date()

        req = self.goal.update_goal()
        if req["successful"]:
            self.on_update()
            self.close_form()
        else:
            CTkMessagebox(title="Error", message=req["message"], icon="cancel")
        




