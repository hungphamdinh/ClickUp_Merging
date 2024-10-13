# gui/pdf_selection.py

import tkinter as tk
from tkinter import messagebox, filedialog  # Import filedialog explicitly
import re
import os
import PyPDF2

class PDFSelectionFrame:
    def __init__(self, parent, gui):
        """
        Initializes the PDFSelectionFrame.

        :param parent: Parent Tkinter widget.
        :param gui: Reference to the main GUI class.
        """
        self.parent = parent
        self.gui = gui
        self.pdf_file = None

        self.create_widgets()

    def create_widgets(self):
        self.pdf_label = tk.Label(self.parent, text="No PDF selected.", fg="red")
        self.pdf_label.pack(anchor=tk.W)

        select_pdf_button = tk.Button(
            self.parent, 
            text="Select PDF", 
            command=self.select_pdf,
            bg="black", fg="white",
            activebackground="grey", activeforeground="white",
            width=15
        )
        select_pdf_button.pack(pady=5)

    def extract_task_ids(self, pdf_file):
        """
        Extracts task IDs from the selected PDF file.

        :param pdf_file: Path to the PDF file.
        :return: Sorted list of unique task IDs.
        """
        task_ids = set()
        try:
            with open(pdf_file, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        # Find all matches of P3-XXXXX
                        matches = re.findall(r'P3-\d+', text)
                        task_ids.update(matches)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract task IDs: {e}")
            return None
        return sorted(list(task_ids))

    def select_pdf(self):
        """
        Handles the selection of the PDF file and extracts task IDs.
        """
        pdf_file = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF files", "*.pdf")])  # Use filedialog directly
        if pdf_file:
            task_ids = self.extract_task_ids(pdf_file)
            if task_ids is not None:
                if not self.gui.git_manager:
                    messagebox.showerror("Error", "Please attach the source code directory first.")
                    return
                self.pdf_file = pdf_file
                self.update_pdf_label()
                # Save task IDs to task_ids.txt in the source code directory
                task_ids_file = os.path.join(self.gui.git_manager.source_code_path, 'task_ids.txt')
                with open(task_ids_file, 'w') as f:
                    for task_id in task_ids:
                        f.write(f"{task_id}\n")
                self.gui.log(f"Extracted {len(task_ids)} task IDs to 'task_ids.txt'.")
                messagebox.showinfo("Success", f"Extracted {len(task_ids)} task IDs to 'task_ids.txt'.")
                # Enable 'Check Branches'
                self.gui.action_buttons.enable_check_branches()
                # Update Task-Branch Display with empty branches initially
                self.gui.update_task_branch_display(task_ids, {})
            else:
                messagebox.showerror("Error", "Failed to extract task IDs.")

    def update_pdf_label(self):
        """
        Updates the PDF file label based on selection.
        """
        if self.pdf_file:
            self.pdf_label.config(text=self.pdf_file, fg="green")
        else:
            self.pdf_label.config(text="No PDF selected.", fg="red")
