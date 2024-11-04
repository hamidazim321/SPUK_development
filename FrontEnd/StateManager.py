import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DB.Tables.users import User


class StateManager:
    def __init__(self):
        self.__state = {
            "is_logged_in": False,
            "user": User("", ""),
        }
        self.subscribers = []

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def notify(self):
        for callback in self.subscribers:
            try:
                callback(self.__state)
            except Exception as e:
                print(f"Error notifying callback: {e}")

    def set_state(self, new_state: dict):
        for key, value in new_state.items():
            if key in self.__state: 
              self.__state[key] = value
        self.notify()

    def get_state(self) -> dict:
        return self.__state
