# gui/action_buttons.py

import tkinter as tk
from tkinter import messagebox

class ActionButtonsFrame:
    def __init__(self, parent, gui):
        """
        Initializes the ActionButtonsFrame.

        :param parent: Parent Tkinter widget.
        :param gui: Reference to the main GUI class.
        """
        self.parent = parent
        self.gui = gui

        self.create_widgets()

    def create_widgets(self):
        # Check Branches Button
        self.check_branches_button = tk.Button(
            self.parent, 
            text="Check Branches", 
            command=self.gui.check_branches, 
            state=tk.DISABLED, 
            width=20,
            bg="black", fg="white",
            activebackground="grey", activeforeground="white"
        )
        self.check_branches_button.pack(side=tk.LEFT, padx=10)

        # Merge Button
        self.merge_button = tk.Button(
            self.parent, 
            text="Merge", 
            command=self.gui.merge_branches, 
            state=tk.DISABLED, 
            width=20,
            bg="black", fg="white",
            activebackground="grey", activeforeground="white"
        )
        self.merge_button.pack(side=tk.LEFT, padx=10)

        # Complete Resolve Button
        self.complete_resolve_button = tk.Button(
            self.parent, 
            text="Complete Resolve", 
            command=self.gui.complete_resolve, 
            state=tk.DISABLED, 
            width=20,
            bg="black", fg="white",
            activebackground="grey", activeforeground="white"
        )
        self.complete_resolve_button.pack(side=tk.LEFT, padx=10)

        # Push Changes Button
        self.push_changes_button = tk.Button(
            self.parent,
            text="Push Changes",
            command=self.gui.push_changes,
            state=tk.DISABLED,  # Initially disabled; enabled after merging
            width=20,
            bg="black", fg="white",
            activebackground="grey", activeforeground="white"
        )
        self.push_changes_button.pack(side=tk.LEFT, padx=10)

    def disable_all_buttons(self):
        """
        Disables all action buttons.
        """
        self.check_branches_button.config(state=tk.DISABLED)
        self.merge_button.config(state=tk.DISABLED)
        self.complete_resolve_button.config(state=tk.DISABLED)
        self.push_changes_button.config(state=tk.DISABLED)

    def enable_check_branches(self):
        """
        Enables the 'Check Branches' button.
        """
        self.check_branches_button.config(state=tk.NORMAL)

    def enable_merge(self):
        """
        Enables the 'Merge' button.
        """
        self.merge_button.config(state=tk.NORMAL)

    def enable_complete_resolve(self):
        """
        Enables the 'Complete Resolve' button.
        """
        self.complete_resolve_button.config(state=tk.NORMAL)

    def disable_complete_resolve(self):
        """
        Disables the 'Complete Resolve' button.
        """
        self.complete_resolve_button.config(state=tk.DISABLED)

    def enable_push_changes(self):
        """
        Enables the 'Push Changes' button.
        """
        self.push_changes_button.config(state=tk.NORMAL)

    def disable_push_changes(self):
        """
        Disables the 'Push Changes' button.
        """
        self.push_changes_button.config(state=tk.DISABLED)
