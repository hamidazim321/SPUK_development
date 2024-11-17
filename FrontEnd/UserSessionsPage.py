from customtkinter import CTkScrollableFrame

class SubjectsPage(CTkScrollableFrame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        self.user_subjects = self.fetch_user_subjects()
        self.state_manager.set_state({"user_subjects": self.user_subjects})
        self.state = self.state_manager.get_state()
        self.subjects_container = None
        self.subject_form = None
        self.load_page()