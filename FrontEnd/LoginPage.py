import tkinter as tk
from tkinter import Frame
from tkinter import messagebox
class LoginPage(Frame):
    def __init__(self, master, state_manager):
        super().__init__(master)
        self.state_manager = state_manager
        self.user = user = self.state_manager.get_state()["user"]
        self.load_page()
    
    def load_page(self):
        # Main frame for the login page content
        subframe = tk.Frame(self)
        subframe.pack(expand=True, fill="both")
        
        # Label for the login page
        label = tk.Label(subframe, text="Login",  font=('Arial', 22))
        label.grid(row=0, column=0, columnspan=2, pady=10)

        # Username frame with label and entry
        username_frame = tk.Frame(subframe)
        username_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        username_label = tk.Label(username_frame, text="Username:", font=('Arial', 12))
        username_label.grid(row=0, column=0, padx=(0, 5))
        username_entry = tk.Entry(username_frame, fg='grey', bg='lightyellow', font=('Arial', 12), borderwidth=2, relief='groove')
        username_entry.insert(0, self.user.name)
        username_entry.grid(row=0, column=1)

        # Password frame with label and entry
        password_frame = tk.Frame(subframe)
        password_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        password_label = tk.Label(password_frame, text="Password:", font=('Arial', 12))
        password_label.grid(row=0, column=0, padx=(0, 5))
        password_entry = tk.Entry(password_frame, show="*", fg='grey', bg='lightyellow', font=('Arial', 12), borderwidth=2, relief='groove')
        password_entry.insert(0, self.user.password)
        password_entry.grid(row=0, column=1)

        btn_frame = tk.Frame(subframe)
        btn_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        login_btn = tk.Button(btn_frame, text="Login", command=lambda:self.login_user(username_entry.get(), password_entry.get()))
        login_btn.grid(row=0, column=0)

    def login_user(self, username, password):
        self.user.name = username
        self.user.password = password
        self.state_manager.set_state({"user":self.user})

        req = self.user.get_user()
        if req["successful"]:
            self.state_manager.set_state({"is_logged_in": True })
        else:
            print(req["message"])
            messagebox.showerror("Error Logging in", "incorrect username or password")
            
