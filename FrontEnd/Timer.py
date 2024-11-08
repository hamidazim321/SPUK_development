import tkinter as tk
from datetime import datetime
import time

class Timer(tk.Label):
    def __init__(self, master, start_time, end_time):
        super().__init__(master, font=("Arial", 12, "bold"))
        self.start_time = start_time
        self.end_time = end_time
        self.update_timer()

    def calculate_time(self):
      elapsed_time = 0
      if self.end_time and self.start_time:
          elapsed_time = (self.end_time - self.start_time).total_seconds()
      elif self.start_time:
          elapsed_time = (datetime.now() - self.start_time).total_seconds()

      minutes = int(elapsed_time // 60)
      seconds = int(elapsed_time % 60)
      return f"{minutes:02}:{seconds:02}"

    def update_timer(self):
        self.config(text=self.calculate_time())
        if not self.end_time:
            self.after(1000, self.update_timer)
