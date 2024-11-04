import tkinter as tk
from tkinter import Frame

class Menu(Frame):
    def __init__(self, master, state_manager, show_frame_callback, pages):
        super().__init__(master)
        self.show_frame_callback = show_frame_callback
        self.state_manager = state_manager
        self.pages = pages
        self.state = self.state_manager.get_state()

        self.load_menu(self.pages)

        self.state_manager.subscribe(self.update_menu)

    def create_button(self, page_name, page_class):
        btn = tk.Button(self, text=page_name, command=lambda: self.show_frame_callback(page_class))
        return btn
    
    def load_menu(self, pages):
        self.state_manager.get_state()
        for widget in self.winfo_children():
            widget.destroy()
        
        if self.state["is_logged_in"]:
            tk.Button(self, text="log out", command=lambda: self.show_frame_callback("HomePage")).pack(side=tk.LEFT, padx=5, pady=5)
        for p in pages:
            btn = self.create_button(p["name"], p["page"])
            btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def update_menu(self, state):
        self.load_menu(self.pages)

    def logout(self):
        print("User logged out")  
        self.show_frame_callback(LoginPage)

