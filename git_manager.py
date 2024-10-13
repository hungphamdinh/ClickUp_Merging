# git_manager.py

import subprocess
import re
import os

class GitManager:
    def __init__(self, source_code_path, log_callback=None):
        """
        Initializes the GitManager with the source code directory.

        :param source_code_path: Path to the Git repository.
        :param log_callback: Optional callback function for logging.
        """
        self.source_code_path = source_code_path
        self.log = log_callback if log_callback else print

    def run_git_command(self, cmd_list):
        """
        Executes a Git command and returns its output.

        :param cmd_list: List of command arguments.
        :return: Command output as a string.
        :raises Exception: If the command fails.
        """
        try:
            result = subprocess.check_output(
                cmd_list,
                cwd=self.source_code_path,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            return result
        except subprocess.CalledProcessError as e:
            raise Exception(e.output)

    def fetch_all(self):
        """Fetches all remote branches."""
        self.log("Fetching all remote branches...")
        self.run_git_command(['git', 'fetch', '--all'])

    def get_merged_branches(self):
        """
        Retrieves a list of all merged branches.

        :return: List of merged branch names.
        """
        self.log("Identifying merged branches...")
        merged_branches_output = self.run_git_command(['git', 'branch', '--all', '--merged'])
        merged_branches = [
            line.strip().replace('remotes/origin/', '').replace('* ', '').strip()
            for line in merged_branches_output.split('\n') if line.strip()
        ]
        merged_branches = list(set(merged_branches))
        return merged_branches

    def get_remote_branches(self):
        """
        Retrieves a list of all remote branches.

        :return: List of remote branch names.
        """
        branch_output = self.run_git_command(['git', 'branch', '-r'])
        remote_branches = re.findall(r'origin/.*', branch_output)
        return remote_branches

    def fetch_specific_branch(self, branch):
        """
        Fetches a specific remote branch.

        :param branch: Branch name to fetch.
        """
        self.log(f"Fetching remote branch '{branch}' from 'origin'...")
        self.run_git_command(['git', 'fetch', 'origin', f"{branch}:{branch}"])

    def is_branch_merged(self, target_branch, current_branch):
        """
        Checks if a branch is already merged into the current branch.

        :param target_branch: Branch to check.
        :param current_branch: Current branch name.
        :return: True if merged, False otherwise.
        """
        is_ancestor = subprocess.call(
            ['git', 'merge-base', '--is-ancestor', target_branch, current_branch],
            cwd=self.source_code_path
        ) == 0
        return is_ancestor

    def merge_branch(self, target_branch, current_branch):
        """
        Merges a target branch into the current branch.

        :param target_branch: Branch to merge.
        :param current_branch: Current branch name.
        :return: True if merge is successful.
        :raises Exception: If a merge conflict occurs.
        """
        self.log(f"🔄 Merging '{target_branch}' into '{current_branch}'...")
        try:
            self.run_git_command([
                'git', 'merge', '--no-ff', target_branch,
                '-m', f"Merge branch '{target_branch}' into '{current_branch}'"
            ])
            self.log(f"🎉 Successfully merged '{target_branch}'.")
            return True
        except Exception as e:
            self.log(f"❌ Merge conflict occurred while merging '{target_branch}'.")
            raise e

    def add_all_changes(self):
        """Stages all changes."""
        self.run_git_command(['git', 'add', '.'])

    def commit_merge(self):
        """Commits the merge without editing the commit message."""
        self.run_git_command(['git', 'commit', '--no-edit'])

    def abort_merge(self):
        """Aborts the current merge."""
        self.run_git_command(['git', 'merge', '--abort'])

    def push_changes(self):
        """Pushes all commits to the remote repository."""
        self.run_git_command(['git', 'push'])

    def get_current_branch(self):
        """
        Retrieves the name of the current branch.

        :return: Current branch name.
        """
        current_branch = self.run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip()
        return current_branch

    def get_task_ids(self, task_ids_file):
        """
        Reads task IDs from a file.

        :param task_ids_file: Path to the task IDs file.
        :return: List of task IDs.
        """
        with open(task_ids_file, 'r') as f:
            task_ids = [line.strip() for line in f if line.strip()]
        return task_ids

    def get_matching_branches(self, task_ids):
        """
        Identifies branches matching the given task IDs.

        :param task_ids: List of task IDs.
        :return: Tuple containing a set of required branches and a mapping of task IDs to branches.
        """
        required_branches = set()
        task_branch_map = {task_id: [] for task_id in task_ids}  # For display
        remote_branches = self.get_remote_branches()

        for task_id in task_ids:
            # Search for matching branches
            matching_branches = re.findall(r'origin/.*' + re.escape(task_id) + r'.*', "\n".join(remote_branches))
            if matching_branches:
                for branch in matching_branches:
                    branch = branch.strip().replace('origin/', '')
                    merged_branches = self.get_merged_branches()
                    if branch not in merged_branches:
                        required_branches.add(branch)
                        task_branch_map[task_id].append(branch)
        return required_branches, task_branch_map

    def write_required_branches(self, required_branches, required_branches_file):
        """
        Writes the required branches to a file.

        :param required_branches: Set of branch names.
        :param required_branches_file: Path to the output file.
        """
        with open(required_branches_file, 'w') as f:
            for branch in required_branches:
                f.write(f"{branch}\n")
