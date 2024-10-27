import tkinter as tk
from tkinter import Frame
from Menu import Menu
from LoginPage import LoginPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sabaq pa Usul Ke")
        self.geometry('600x600')

        self.menu = Menu(self, self.show_frame)
        self.menu.pack(side=tk.TOP, fill=tk.X) 

        self.current_frame = None
        self.show_frame(LoginPage)  

    def show_frame(self, frame_class):
        """Show a frame for the given class."""
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
