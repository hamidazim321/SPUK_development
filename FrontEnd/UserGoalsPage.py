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

        self.title_label = None
        self.description_label = None
        self.status_label = None

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
        self.status_label.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        self.description_label = CTkLabel(self, anchor="w", wraplength=300)
        self.description_label.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

        CTkButton(
            self,
            text="Achieved",
            fg_color="green",
            hover_color="#33cc33",
        ).grid(row=2, column=2, sticky="e", padx=10, pady=5)

        update_remove_btns_frame = CTkFrame(self)
        update_remove_btns_frame.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        CTkButton(
            update_remove_btns_frame,
            text="Update",
        ).grid(row=0, column=0, padx=5, pady=3)

        CTkButton(
            update_remove_btns_frame,
            text="Delete",
            fg_color="red",
            hover_color="#ff4d4d",
            command=self.__remove_card
        ).grid(row=0, column=1, padx=5, pady=3)

    def __load_data(self):
        self.title_label.configure(text=self.goal.title)
        self.description_label.configure(text=self.goal.description)
        self.__set_card_status()

    def __set_card_status(self):
        if isinstance(self.goal.due_date, str):
            try:
                goal_due_date = datetime.strptime(self.goal.due_date, "%Y-%m-%d").date()
            except ValueError:
                goal_due_date = datetime.strptime(self.goal.due_date, "%d/%m/%Y").date()
        elif isinstance(self.goal.due_date, date):
            goal_due_date = self.goal.due_date 
        else:
            raise TypeError("Invalid due_date format")

        current_date = datetime.today().date()
        if self.goal.achieved:
            self.configure(border_color="green")
            self.status_label.configure(text="achieved", text_color="green")
        elif goal_due_date > current_date:
            self.configure(border_color="blue")
            self.status_label.configure(text="upcoming", text_color="blue")
        else:
            self.configure(border_color="red")
            self.status_label.configure(text="overdue", text_color="red" )

    
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

class AddGoalForm(CTkToplevel):
    def __init__(self, master, on_add):
        super().__init__(master)
        self.title("Add a goal")
        self.geometry("400x300")
        self.on_add = on_add
    
        self.__create_form()
    def __create_form(self):
        title_entry = CTkEntry(self, placeholder_text="title")
        title_entry.grid(row=0, column=0, sticky="ew", padx=10)

        description_box = CTkTextbox(self)
        description_box.grid(row=1, column=0, sticky="ew")

        date_picker = DatePicker(self)
        date_picker.set_placeholder("Select due date")
        date_picker.grid(row=2, column=0, sticky="ew")

        CTkButton(self, text="Add", command=lambda:self.__add_goal(
            title_entry, description_box, date_picker
        )).grid(row=3, column=0)
    
    def __add_goal(self, title_entry, description_box, date_picker):
        date_error = self.__check_date(date_picker.get_date())

        if date_error:
            CTkMessagebox(title="Incorrect date format", message=date_error, icon="cancel")
            return

        title = title_entry.get()
        description = description_box.get("0.0", "end").strip()
        due_date = datetime.strptime(date_picker.get_date(), date_picker.date_format).date()

        goal = UserGoal(title=title, description=description, due_date=due_date)
        req = goal.add_goal()
        if req["successful"]:
            self.on_add(goal)
            self.__close_form()
        else:
            CTkMessagebox("Error adding goal", message=req["message"], icon="cancel")
        return
    
    def __close_form(self):
        self.after(300, self.destroy)
    
    def __check_date(self,date):
        error = None
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d")
            return None
        except ValueError:
            return "Date must be in the format yyyy-mm-dd" 
    

        




