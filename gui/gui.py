# gui/gui.py

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
from .source_selection import SourceSelectionFrame
from .pdf_selection import PDFSelectionFrame
from .task_branch_display import TaskBranchDisplayFrame
from .action_buttons import ActionButtonsFrame
from .log_area import LogAreaFrame
from git_manager import GitManager

class GitMergeToolkitGUI:
    def __init__(self, root):
        self.root = root
        self.git_manager = None  # Will be initialized upon selecting source code directory

        # Initialize main frames
        self.create_frames()

        # Initialize GUI components
        self.source_selection = SourceSelectionFrame(self.source_frame, self)
        self.pdf_selection = PDFSelectionFrame(self.pdf_frame, self)
        self.task_branch_display = TaskBranchDisplayFrame(self.display_frame, self)
        self.action_buttons = ActionButtonsFrame(self.actions_frame, self)
        self.log_area = LogAreaFrame(self.log_frame, self)

    def create_frames(self):
        # Top Frame for Guide Text
        self.top_frame = tk.Frame(self.root, padx=10, pady=10)
        self.top_frame.pack(fill=tk.X)

        # Create Guide Text
        self.create_guide_text()

        # Middle Frame for Source Code and PDF Selection
        self.middle_frame = tk.Frame(self.root, padx=10, pady=10)
        self.middle_frame.pack(fill=tk.X)

        # Sub-frames within middle_frame
        self.source_frame = tk.LabelFrame(self.middle_frame, text="Source Code", padx=10, pady=10)
        self.source_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.pdf_frame = tk.LabelFrame(self.middle_frame, text="PDF File", padx=10, pady=10)
        self.pdf_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Bottom Frame for Actions and Logs
        self.bottom_frame = tk.Frame(self.root, padx=10, pady=10)
        self.bottom_frame.pack(fill=tk.BOTH, expand=True)

        # Sub-frames within bottom_frame
        self.display_frame = tk.LabelFrame(self.bottom_frame, text="Task IDs and Associated Branches", padx=10, pady=10)
        self.display_frame.pack(fill=tk.BOTH, expand=True)

        self.actions_frame = tk.Frame(self.bottom_frame, pady=10)
        self.actions_frame.pack()

        self.log_frame = tk.LabelFrame(self.bottom_frame, text="Logs", padx=10, pady=10)
        self.log_frame.pack(fill=tk.BOTH, expand=True, pady=(10,0))

    def create_guide_text(self):
        guide_text = (
            "Git Merge Toolkit Guide:\n\n"
            "1. **Select Source Code Directory**:\n"
            "   - Click the 'Select Source Code Directory' button.\n"
            "   - Choose the root directory of your Git repository.\n\n"
            "2. **Select PDF File**:\n"
            "   - Click the 'Select PDF' button.\n"
            "   - Choose the PDF containing task IDs in the format 'P3-XXXXX'.\n\n"
            "3. **Check Branches**:\n"
            "   - Click the 'Check Branches' button to identify branches related to the task IDs.\n\n"
            "4. **Merge Branches**:\n"
            "   - Click the 'Merge' button to merge the identified branches into your current branch.\n"
            "   - If merge conflicts occur, resolve them in the source code directory and click 'Complete Resolve' to finalize.\n\n"
            "5. **Push Changes**:\n"
            "   - After merging, click the 'Push Changes' button to push all committed changes to the remote repository."
        )
        # Use Text widget for multi-line, read-only guide
        self.guide_text_widget = tk.Text(
            self.top_frame, 
            height=15, 
            wrap=tk.WORD, 
            padx=5, 
            pady=5, 
            bg=self.root.cget('bg'), 
            relief=tk.FLAT
        )
        self.guide_text_widget.insert(tk.END, guide_text)
        self.guide_text_widget.configure(state='disabled')  # Make read-only
        self.guide_text_widget.pack(fill=tk.BOTH)

    def log(self, message):
        """
        Appends a message to the log area.

        :param message: Message string to log.
        """
        self.log_area.log(message)

    def update_task_branch_display(self, task_ids, task_branch_map):
        """
        Updates the Task IDs and Branches display.

        :param task_ids: List of task IDs.
        :param task_branch_map: Dictionary mapping task IDs to branches.
        """
        self.task_branch_display.update_display(task_ids, task_branch_map)

    # Methods invoked by action buttons

    def check_branches(self, from_resolve=False):
        """
        Initiates the branch checking process.

        :param from_resolve: Boolean indicating if the method is called after resolving conflicts.
        """
        if not from_resolve:
            # Disable buttons to prevent multiple operations only if not called from resolve
            self.action_buttons.disable_all_buttons()
        else:
            # Optionally, disable specific buttons or show a loading indicator
            pass

        # Clear previous display
        self.update_task_branch_display([], {})
        # Run in a separate thread to keep GUI responsive
        threading.Thread(target=self._check_branches, daemon=True).start()


    def _check_branches(self):
        """
        Performs the actual branch checking in a separate thread.
        """
        try:
            if not self.git_manager:
                self.log("Error: Source code directory not attached.")
                return

            self.log("Starting branch check...")
            task_ids_file = os.path.join(self.git_manager.source_code_path, 'task_ids.txt')
            required_branches_file = os.path.join(self.git_manager.source_code_path, 'required_branches.txt')

            if not os.path.exists(task_ids_file):
                self.log("Error: task_ids.txt not found in the source code directory. Please extract task IDs first.")
                return

            task_ids = self.git_manager.get_task_ids(task_ids_file)

            self.git_manager.fetch_all()

            required_branches, task_branch_map = self.git_manager.get_matching_branches(task_ids)

            # Write required branches to required_branches.txt
            self.git_manager.write_required_branches(required_branches, required_branches_file)

            self.log(f"Found {len(required_branches)} required branches.")
            messagebox.showinfo("Success", f"Found {len(required_branches)} required branches.")

            # Update Task-Branch Display
            self.update_task_branch_display(task_ids, task_branch_map)

            # Enable 'Merge' button if there are branches to merge
            if required_branches:
                self.action_buttons.enable_merge()
            else:
                self.action_buttons.disable_merge()

            if self.status_label:
                self.status_label.config(text="Status: Branch check completed.")

        except Exception as e:
            self.log(f"Error during branch check: {e}")
            messagebox.showerror("Error", f"An error occurred during branch check:\n{e}")
        finally:
            if not from_resolve:
                self.action_buttons.enable_all_buttons()
            else:
                # Optionally, handle button states if called from resolve
                pass


    def merge_branches(self):
        """
        Initiates the merge process.
        """
        # Disable buttons to prevent multiple operations
        self.action_buttons.disable_all_buttons()
        # Run in a separate thread to keep GUI responsive
        threading.Thread(target=self._merge_branches).start()

    def _merge_branches(self):
        """
        Performs the actual merging in a separate thread.
        """
        try:
            if not self.git_manager:
                messagebox.showerror("Error", "Please attach the source code directory first.")
                self.action_buttons.enable_merge()
                return

            self.log("Starting merge process...")
            required_branches_file = os.path.join(self.git_manager.source_code_path, 'required_branches.txt')

            if not os.path.exists(required_branches_file):
                messagebox.showerror("Error", "required_branches.txt not found in the source code directory. Please check branches first.")
                self.action_buttons.enable_merge()
                return

            with open(required_branches_file, 'r') as f:
                required_branches = [line.strip() for line in f if line.strip()]

            if not required_branches:
                self.log("No required branches to merge.")
                messagebox.showinfo("Info", "No required branches to merge.")
                self.action_buttons.enable_merge()
                return

            # Determine the current branch
            current_branch = self.git_manager.get_current_branch()
            if not current_branch:
                messagebox.showerror("Error", "Unable to determine the current branch.")
                self.action_buttons.enable_merge()
                return
            self.log(f"Current branch: '{current_branch}'")

            already_merged = []
            merged_now = []
            failed_merges = []

            for branch in required_branches:
                self.log(f"Processing branch: '{branch}'")

                # Check if branch is already merged
                if self.git_manager.is_branch_merged(branch, current_branch):
                    self.log(f"✅ Branch '{branch}' is already merged into '{current_branch}'. Skipping.")
                    already_merged.append(branch)
                    continue

                # Check if branch exists locally or remotely
                branch_exists = False
                local_branch = False
                try:
                    # Check if branch exists locally
                    self.git_manager.run_git_command(['git', 'show-ref', '--verify', '--quiet', f"refs/heads/{branch}"])
                    branch_exists = True
                    local_branch = True
                    self.log(f"Found '{branch}' as a local branch.")
                except Exception:
                    try:
                        # Check if branch exists remotely
                        self.git_manager.run_git_command(['git', 'show-ref', '--verify', '--quiet', f"refs/remotes/origin/{branch}"])
                        branch_exists = True
                        local_branch = False
                        self.log(f"Found '{branch}' as a remote branch.")
                        # Fetch the specific remote branch to ensure it's up-to-date
                        self.git_manager.fetch_specific_branch(branch)
                    except Exception:
                        pass

                if not branch_exists:
                    self.log(f"⚠️  Branch '{branch}' does not exist locally or remotely. Skipping.")
                    failed_merges.append(branch)
                    continue

                target_branch = branch if local_branch else f"origin/{branch}"

                # Attempt to merge the branch
                try:
                    self.git_manager.merge_branch(target_branch, current_branch)
                    merged_now.append(branch)
                except Exception as e:
                    self.log(f"❌ Merge conflict occurred while merging '{branch}'.")
                    # Set conflict state
                    self.conflict_occurred = True
                    self.current_conflict_branch = branch
                    # Enable 'Complete Resolve' button
                    self.action_buttons.enable_complete_resolve()
                    # Inform the user about the conflict
                    messagebox.showwarning(
                        "Merge Conflict",
                        f"Merge conflict occurred while merging '{branch}'.\n\n"
                        "Please resolve the conflicts in the source code directory and then click 'Complete Resolve' to finalize the merge."
                    )
                    self.log("Merge process paused due to conflicts.")
                    return  # Exit the merge process until conflicts are resolved

            # Show summary if no conflicts occurred
            summary = "Merge Summary:\n"
            if already_merged:
                summary += "\n✅ Already Merged:\n"
                for b in already_merged:
                    summary += f"  - {b}\n"
            if merged_now:
                summary += "\n🎉 Merged Now:\n"
                for b in merged_now:
                    summary += f"  - {b}\n"
            if failed_merges:
                summary += "\n❌ Failed to Merge:\n"
                for b in failed_merges:
                    summary += f"  - {b}\n"
                summary += "\nSome branches failed to merge. Please resolve conflicts and merge them manually."
                self.log(summary)
                messagebox.showwarning("Merge Summary", summary)
            else:
                summary += "\nAll required branches have been successfully merged."
                self.log(summary)
                messagebox.showinfo("Merge Summary", summary)
                # Enable 'Push Changes' button after successful merge
                self.action_buttons.enable_push_changes()

        except Exception as e:
            self.log(f"❌ An error occurred during merging: {e}")
            messagebox.showerror("Error", f"An error occurred during merging:\n{e}")
        finally:
            if not hasattr(self, 'conflict_occurred') or not self.conflict_occurred:
                self.action_buttons.enable_merge()


    def complete_resolve(self):
        """
        Finalizes the merge after resolving conflicts by committing the resolved changes.
        Does not push the changes automatically.
        """
        try:
            if not self.conflict_occurred or not self.current_conflict_branch:
                messagebox.showinfo("Info", "No merge conflicts to resolve.")
                return

            self.log(f"Attempting to finalize merge for '{self.current_conflict_branch}'...")

            # Add all changes
            self.git_manager.add_all_changes()

            # Commit the merge with a specific commit message
            commit_message = "Resolve merge conflict"
            self.git_manager.commit_merge(commit_message)

            self.log(f"🎉 Conflicts resolved and '{self.current_conflict_branch}' merged.")
            messagebox.showinfo("Success", f"Conflicts resolved and '{self.current_conflict_branch}' merged successfully.")

            # Reset conflict state
            self.conflict_occurred = False
            self.current_conflict_branch = None

            # Disable 'Complete Resolve' button
            self.action_buttons.disable_complete_resolve()

            # Notify user to push changes manually
            self.log("Please push your changes to the remote repository when ready.")
            messagebox.showinfo("Info", "Please push your changes to the remote repository when ready.")

            # Refresh merge summary and update GUI
            self.log("Finalizing merge process...")
            self._finalize_merge()

            # Restart branch checking to update the display
            self.check_branches(from_resolve=True)

        except Exception as e:
            self.log(f"❌ Failed to finalize merge after conflict resolution: {e}")
            messagebox.showerror("Error", f"Failed to finalize merge after conflict resolution:\n{e}")
            # Abort the merge to clean up
            if self.current_conflict_branch:
                try:
                    self.git_manager.abort_merge()
                    self.log(f"🛑 Merge aborted for '{self.current_conflict_branch}'.")
                except Exception:
                    self.log(f"🛑 Failed to abort merge for '{self.current_conflict_branch}'.")
            else:
                self.log("🛑 Failed to abort merge: No conflict branch specified.")
                messagebox.showerror("Error", "Failed to abort merge: No conflict branch specified.")
        messagebox.showerror("Error", "Failed to abort merge: No conflict branch specified.")

    def _finalize_merge(self):
        """
        Finalizes the merge by processing remaining branches after conflict resolution.
        """
        try:
            required_branches_file = os.path.join(self.git_manager.source_code_path, 'required_branches.txt')
            if not os.path.exists(required_branches_file):
                return

            with open(required_branches_file, 'r') as f:
                required_branches = [line.strip() for line in f if line.strip()]

            if not required_branches:
                return

            # Determine the current branch
            current_branch = self.git_manager.get_current_branch()
            if not current_branch:
                return

            already_merged = []
            merged_now = []
            failed_merges = []

            # Since we have already merged the conflicting branch, remove it from the list
            # and continue merging the remaining branches
            if self.current_conflict_branch and self.current_conflict_branch in required_branches:
                required_branches.remove(self.current_conflict_branch)

            for branch in required_branches:
                self.log(f"Processing branch: '{branch}'")
                # Check if branch exists locally or remotely
                branch_exists = False
                local_branch = False
                try:
                    # Check if branch exists locally
                    self.git_manager.run_git_command(['git', 'show-ref', '--verify', '--quiet', f"refs/heads/{branch}"])
                    branch_exists = True
                    local_branch = True
                    self.log(f"Found '{branch}' as a local branch.")
                except Exception:
                    try:
                        # Check if branch exists remotely
                        self.git_manager.run_git_command(['git', 'show-ref', '--verify', '--quiet', f"refs/remotes/origin/{branch}"])
                        branch_exists = True
                        local_branch = False
                        self.log(f"Found '{branch}' as a remote branch.")
                        # Fetch the specific remote branch to ensure it's up-to-date
                        self.git_manager.fetch_specific_branch(branch)
                    except Exception:
                        pass

                if not branch_exists:
                    self.log(f"⚠️  Branch '{branch}' does not exist locally or remotely. Skipping.")
                    failed_merges.append(branch)
                    continue

                target_branch = branch if local_branch else f"{branch}"

                # Check if the branch is already merged
                is_ancestor = self.git_manager.is_branch_merged(target_branch, current_branch)
                if is_ancestor:
                    self.log(f"✅ Branch '{branch}' is already merged into '{current_branch}'.")
                    already_merged.append(branch)
                    continue

                # Attempt to merge the branch
                try:
                    self.git_manager.merge_branch(target_branch, current_branch)
                    merged_now.append(branch)
                except Exception as e:
                    self.log(f"❌ Merge conflict occurred while merging '{branch}'.")
                    failed_merges.append(branch)
                    # Optionally, handle further conflicts or notify the user
                    messagebox.showwarning(
                        "Merge Conflict",
                        f"Merge conflict occurred while merging '{branch}'.\n\n"
                        "Please resolve the conflicts in the source code directory and re-run the merge process."
                    )

            # Show summary
            summary = "Merge Summary:\n"
            if already_merged:
                summary += "\n✅ Already Merged:\n"
                for b in already_merged:
                    summary += f"  - {b}\n"
            if merged_now:
                summary += "\n🎉 Merged Now:\n"
                for b in merged_now:
                    summary += f"  - {b}\n"
            if failed_merges:
                summary += "\n❌ Failed to Merge:\n"
                for b in failed_merges:
                    summary += f"  - {b}\n"
                summary += "\nSome branches failed to merge. Please resolve conflicts and merge them manually."
                self.log(summary)
                messagebox.showwarning("Merge Summary", summary)
            else:
                summary += "\nAll required branches have been successfully merged."
                self.log(summary)
                messagebox.showinfo("Merge Summary", summary)
                # Enable 'Push Changes' button after successful merge
                self.action_buttons.enable_push_changes()

        except Exception as e:
            self.log(f"❌ An error occurred during finalizing the merge: {e}")
            messagebox.showerror("Error", f"An error occurred during finalizing the merge:\n{e}")

    # Inside GitMergeToolkitGUI class

    def push_changes(self):
        """
        Initiates the push process.
        """
        # Disable buttons to prevent multiple operations
        self.action_buttons.disable_all_buttons()
        # Run in a separate thread to keep GUI responsive
        threading.Thread(target=self._push_changes, daemon=True).start()

    def _push_changes(self):
        """
        Performs the actual push operation in a separate thread.
        """
        try:
            if not self.git_manager:
                messagebox.showerror("Error", "Please attach the source code directory first.")
                self.action_buttons.enable_all_buttons()
                return

            self.log("Starting push process...")
            # Push all commits to the remote repository
            self.git_manager.push_changes()
            self.log("🎉 Successfully pushed all changes to the remote repository.")
            messagebox.showinfo("Success", "Successfully pushed all changes to the remote repository.")
        except Exception as e:
            self.log(f"❌ Failed to push changes: {e}")
            messagebox.showerror("Error", f"Failed to push changes:\n{e}")
            # Re-enable the push button to allow retry
            self.action_buttons.enable_push_changes()
        finally:
            # Ensure other buttons are re-enabled
            self.action_buttons.enable_all_buttons()

    def _refresh_branch_display(self):
        """
        Refreshes the Task IDs and Branches display to reflect the latest state.
        """
        try:
            task_ids_file = os.path.join(self.git_manager.source_code_path, 'task_ids.txt')
            required_branches_file = os.path.join(self.git_manager.source_code_path, 'required_branches.txt')

            if not os.path.exists(task_ids_file) or not os.path.exists(required_branches_file):
                self.log("Task IDs or Required Branches file not found. Skipping display refresh.")
                return

            task_ids = self.git_manager.get_task_ids(task_ids_file)
            required_branches, task_branch_map = self.git_manager.get_matching_branches(task_ids)

            # Update Task-Branch Display
            self.update_task_branch_display(task_ids, task_branch_map)

            self.log("Branch display refreshed.")
        except Exception as e:
            self.log(f"❌ Failed to refresh branch display: {e}")
            messagebox.showerror("Error", f"Failed to refresh branch display:\n{e}")
