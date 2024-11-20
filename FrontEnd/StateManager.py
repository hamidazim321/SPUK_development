from DB.Queries.user import User


class StateManager:
    def __init__(self):
        self.__state = {
            "is_logged_in": False,
            "user": User("", ""),
            "user_subjects": [],
            "current_session": None,
            "user_sessions": [],
            "user_goals": []
        }
        self.subscribers = []

    def subscribe(self, callback, on_change_attributes, context):
        self.subscribers.append({
            "callback": callback,
            "on_change_attributes": on_change_attributes,
            "context": context
        })
        
    def unsubscribe(self, context):
        self.subscribers = [sub for sub in self.subscribers if sub["context"] != context]


    def notify(self, attributes: list):
        for subscriber in self.subscribers:
            if any(attr in subscriber["on_change_attributes"] for attr in attributes):
                try:
                    subscriber["callback"](self.__state.copy())
                except Exception as e:
                    print(f"Error notifying callback: {e}")

    def set_state(self, new_state: dict):
        changed_attributes = []

        for key, value in new_state.items():
            if key in self.__state:
                self.__state[key] = value
                changed_attributes.append(key)
        if changed_attributes:
            self.notify(changed_attributes)

    def get_state(self) -> dict:
        return self.__state.copy()
