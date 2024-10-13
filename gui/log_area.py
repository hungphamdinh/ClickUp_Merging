# gui/log_area.py

import tkinter as tk
from tkinter import ttk

class LogAreaFrame:
    def __init__(self, parent, gui):
        """
        Initializes the LogAreaFrame.

        :param parent: Parent Tkinter widget.
        :param gui: Reference to the main GUI class.
        """
        self.parent = parent
        self.gui = gui

        self.create_widgets()

    def create_widgets(self):
        self.log_text = tk.Text(self.parent, height=15, wrap=tk.WORD, state='disabled', bg="#f0f0f0")
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        """
        Appends a message to the log area.

        :param message: Message string to log.
        """
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.configure(state='disabled')
        self.log_text.see(tk.END)
