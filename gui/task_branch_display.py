# gui/task_branch_display.py

import tkinter as tk
from tkinter import ttk

class TaskBranchDisplayFrame:
    def __init__(self, parent, gui):
        """
        Initializes the TaskBranchDisplayFrame.

        :param parent: Parent Tkinter widget.
        :param gui: Reference to the main GUI class.
        """
        self.parent = parent
        self.gui = gui

        self.create_widgets()

    def create_widgets(self):
        columns = ("Task ID", "Branches")
        self.tree = ttk.Treeview(self.parent, columns=columns, show='headings')
        self.tree.heading("Task ID", text="Task ID")
        self.tree.heading("Branches", text="Branches")
        self.tree.column("Task ID", width=150, anchor=tk.CENTER)
        self.tree.column("Branches", width=700, anchor=tk.W)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.parent, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def update_display(self, task_ids, task_branch_map):
        """
        Updates the Treeview with Task IDs and their associated branches.

        :param task_ids: List of task IDs.
        :param task_branch_map: Dictionary mapping task IDs to branches.
        """
        # Clear existing entries
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Populate Treeview
        for task_id in task_ids:
            branches = ", ".join(task_branch_map.get(task_id, []))
            self.tree.insert("", tk.END, values=(task_id, branches))
