import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DB.Queries.user import User


class StateManager:
    def __init__(self):
        self.__state = {
            "is_logged_in": False,
            "user": User("", ""),
            "user_subjects": [],
            "current_session": None,
            "user_sessions": []
        }
        self.subscribers = []

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def notify(self):
        for callback in self.subscribers:
            try:
                callback(self.__state.copy())
            except Exception as e:
                print(f"Error notifying callback: {e}")
                print(callback)

    def set_state(self, new_state: dict):
        for key, value in new_state.items():
            if key in self.__state: 
              self.__state[key] = value
        self.notify()

    def get_state(self) -> dict:
        return self.__state.copy()
