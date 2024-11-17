from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from  CTkMessagebox import  CTkMessagebox

class LoginPage(CTkFrame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        self.user = self.state_manager.get_state()["user"]
        self.load_page()

    def load_page(self):
        # Main frame for the login page content
        subframe = CTkFrame(self)
        subframe.pack(pady=20, padx=20)

        # Label for the login page
        label = CTkLabel(subframe, text="Login or Sign up", font=('Arial', 22))
        label.grid(row=0, column=0, columnspan=2, pady=10)

        # Username frame with label and entry
        self.username_entry = CTkEntry(subframe, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=(5, 0), pady=5, sticky="ew")

        # Password frame with label and entry
        self.password_entry = CTkEntry(subframe, show="*", placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=(5, 0), pady=5, sticky="ew")

        # Buttons frame
        btn_frame = CTkFrame(subframe)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        login_btn = CTkButton(btn_frame, text="Login", command=self.login_user)
        login_btn.grid(row=0, column=0, padx=5)

        sign_up_btn = CTkButton(btn_frame, text="Sign Up", command=self.sign_up)
        sign_up_btn.grid(row=0, column=1, padx=5)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.user.username = username
        self.user.password = password
        self.state_manager.set_state({"user": self.user})

        req = self.user.login_user()
        if req["successful"]:
            self.state_manager.set_state({"is_logged_in": True})
        else:
            print(req["message"])
            CTkMessagebox.show_error(title="Error Logging in", message="Incorrect username or password")

    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.user.username = username
        self.user.password = password
        req = self.user.create_user()
        if req["successful"]:
            self.state_manager.set_state({"is_logged_in": True, "user": self.user})
        else:
            print(req["message"])
            CTkMessagebox.show_error(title="Error Signing up", message="User already exists")
