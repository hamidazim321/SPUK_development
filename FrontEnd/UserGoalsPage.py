from customtkinter import CTkScrollableFrame, CTkFrame, CTkToplevel, CTkLabel, CTkEntry, CTkButton, CTkTextbox
from CTkMessagebox import CTkMessagebox
from Components.DatePicker import DatePicker
from datetime import datetime
from DB.Queries.user_goal import UserGoal


class GoalsPage(CTkScrollableFrame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        self.user_goals = self.fetch_user_goals()
        self.state_manager.set_state({"user_goals": self.user_goals})

    def fetch_user_goals(self):
        user_goal = UserGoal()
        req = user_goal.get_all_goals()
        if req["successful"]:
            return req["goals"]
        else:
            CTkMessagebox(title="Error fetching goals", message=req["message"], icon="cancel")
            return []

