# gui/source_selection.py

import tkinter as tk
from tkinter import messagebox, filedialog  # Import filedialog explicitly
from tkinter import ttk
import os
from git_manager import GitManager  # Ensure GitManager is imported
from .button_utils import create_styled_button  # Import the utility function

class SourceSelectionFrame:
    def __init__(self, parent, gui):
        """
        Initializes the SourceSelectionFrame.

        :param parent: Parent Tkinter widget.
        :param gui: Reference to the main GUI class.
        """
        self.parent = parent
        self.gui = gui
        self.source_code_path = None

        self.create_widgets()

    def create_widgets(self):
        self.source_label = tk.Label(self.parent, text="No repository attached.", fg="red")
        self.source_label.pack(anchor=tk.W)

        # Create 'Select Source Code Directory' button using the utility function
        select_source_button = create_styled_button(
            parent=self.parent,
            text="Select Source Code Directory",
            command=self.select_source_code,
            width=25
        )
        select_source_button.pack(pady=5)

    def select_source_code(self):
        """
        Handles the selection of the source code directory.
        """
        source_code_dir = filedialog.askdirectory(title="Select Source Code Directory")  # Use filedialog directly
        if source_code_dir:
            if os.path.isdir(source_code_dir):
                # Check if it's a Git repository
                if os.path.exists(os.path.join(source_code_dir, '.git')):
                    self.source_code_path = source_code_dir
                    self.update_source_label()
                    self.gui.log(f"Source code directory attached: {self.source_code_path}")
                    messagebox.showinfo("Success", f"Source code directory attached:\n{self.source_code_path}")
                    # Initialize GitManager if not already done
                    if not self.gui.git_manager:
                        self.gui.git_manager = GitManager(source_code_dir, self.gui.log)
                    # Enable 'Check Branches' if PDF is already selected
                    if self.gui.pdf_selection.pdf_file:
                        self.gui.action_buttons.enable_check_branches()
                else:
                    messagebox.showerror("Error", "Selected directory is not a Git repository.")
                    self.source_code_path = None
                    self.update_source_label()
            else:
                messagebox.showerror("Error", "Selected path is not a directory.")
                self.source_code_path = None
                self.update_source_label()

    def update_source_label(self):
        """
        Updates the source code directory label based on selection.
        """
        if self.source_code_path:
            self.source_label.config(text=self.source_code_path, fg="green")
        else:
            self.source_label.config(text="No repository attached.", fg="red")
