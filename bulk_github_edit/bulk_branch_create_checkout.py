"""
Git Branch Automation Script

This script automates the process of creating and switching to a new Git branch 
across multiple repositories within a specified parent folder. It performs the following tasks:

1. Iterates through all subdirectories of the given parent folder, assuming each is a
Git repository.
2. Checks if the directory is a valid Git repository.
3. Creates and switches to the specified branch in each repository.

Modules Required:
- os: For file system navigation.
- subprocess: For executing Git commands.

Functions:
- create_and_switch_branch(repo_path, branch_name): 
  Creates a new Git branch and switches to it within a given repository.
- automate_branch_creation(parent_folder, branch_name): 
  Iterates through repositories in a given parent folder and creates the specified branch.

Usage:
Run the script and provide the required inputs:
1. Parent folder containing Git repositories.
2. The name of the branch to create and switch to.

Example:
$ python automate_branch.py
Enter the path to the folder containing your Git repositories: /path/to/repos
Enter the name of the new branch: feature-branch

Notes:
- The script assumes each subdirectory in the parent folder is a Git repository.
- It skips directories that are not valid Git repositories (i.e., missing a `.git` folder).
- The script does not check for existing branches before creating a new one.

Author: Brian Kenkel
"""

import os
import subprocess

def print_separator():
    """
    Prints a separator line.
    """
    print("\n")
    print("----------")
    print("\n")

def push_branch(repo_path):
    """
    Push the current branch to the remote repository and set upstream tracking.
    """
    try:
        os.chdir(repo_path)

        # Get the current branch name
        result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], 
                                capture_output=True, text=True, check=True)
        current_branch = result.stdout.strip()

        # Push branch to remote
        subprocess.run(["git", "push", "--set-upstream", "origin", current_branch], check=True)

        print(f"Pushed and set upstream for branch '{current_branch}' in {repo_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error pushing branch in {repo_path}: {e}")
        raise

def create_and_switch_branch(repo_path, branch_name):
    """
    Create a new branch and switch to it in the given repository.
    """
    try:
        # Navigate to the repository directory
        os.chdir(repo_path)

        # Check if the directory is a Git repository
        if not os.path.isdir(".git"):
            print(f"Skipping {repo_path}: Not a Git repository.")
            return

        # Create and switch to the new branch
        print(f"Creating new branch, '{branch_name}', in {repo_path}")
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error in {repo_path}: {e}")
    except Exception as e:
        print(f"Unexpected error in {repo_path}: {e}")

    print("\n")

def automate_branch_creation(parent_folder, branch_name):
    """
    Automate branch creation in all Git repositories inside the parent folder.
    """
    # Loop through all directories in the parent folder
    for root, dirs, files in os.walk(parent_folder):
        for dir_name in dirs:
            repo_path = os.path.join(root, dir_name)
            create_and_switch_branch(repo_path, branch_name)
            push_branch(repo_path)
        break  # Prevent walking into subdirectories

    print("\n")

if __name__ == "__main__":
    os.system('clear')

    # Prompt the user for the parent folder path
    parent_folder = input("Enter the path to the folder containing your Git repositories: ").strip()

    # Validate the path
    if not os.path.isdir(parent_folder):
        print(f"The path '{parent_folder}' does not exist or is not a directory.")
        exit(1)

    # Prompt the user for the new branch name
    branch_name = input("Enter the name of the new branch: ").strip()

    if not branch_name:
        print("Branch name cannot be empty!")
    else:
        print_separator()
        automate_branch_creation(parent_folder, branch_name)
