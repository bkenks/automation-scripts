"""
Automates copying a folder into multiple Git repositories, staging the changes, committing, and
pushing them.

This script:
1. Prompts the user for:
   - A parent directory containing multiple Git repositories.
   - A source folder to copy into each repository.
   - A commit message for the changes.
2. Iterates through each subdirectory in the parent folder.
3. Copies the source folder into each Git repository.
4. Stages, commits, and pushes the changes.

Functions:
- copy_folder_to_repos(source_folder, repo_path): Copies the source folder into a given repository.
- stage_commit_and_push(repo_path, commit_message): Stages, commits, and pushes changes in a
repository.
- automate_folder_copy_and_push(parent_folder, source_folder, commit_message): Orchestrates the
automation for all repositories.

Usage:
Run the script and provide the necessary inputs when prompted.

Note:
- Skips directories that are not Git repositories.
- Skips repositories where the folder already exists.
- Prints errors but continues processing other repositories.
"""

import os
import shutil
import subprocess

def print_separator():
    """
    Prints a separator line.
    """
    print("\n")
    print("----------")
    print("\n")

def copy_folder_to_repos(source_folder, repo_path):
    """
    Copy the source folder into the specified repository.
    """
    try:
        # Get the name of the source folder
        folder_name = os.path.basename(source_folder)
        
        # Define the destination path in the repository
        destination_path = os.path.join(repo_path, folder_name)
        
        # Copy the folder (and its contents) to the repository
        if os.path.exists(destination_path):
            print(f"Folder '{folder_name}' already exists in {repo_path}. Skipping copy.")
        else:
            shutil.copytree(source_folder, destination_path)
            print(f"Copied '{folder_name}' to {repo_path}")
    except Exception as e:
        print(f"Error copying folder to {repo_path}: {e}")
        raise

def stage_commit_and_push(repo_path, commit_message):
    """
    Stage, commit, and push changes in the specified repository.
    """
    try:
        # Navigate to the repository directory
        os.chdir(repo_path)

        # Check if the directory is a Git repository
        if not os.path.isdir(".git"):
            print(f"Skipping {repo_path}: Not a Git repository.")
            return

        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)

        # Commit the changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push the changes
        subprocess.run(["git", "push"], check=True)
        print(f"Pushed changes in {repo_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error in {repo_path}: {e}")
    except Exception as e:
        print(f"Unexpected error in {repo_path}: {e}")

def automate_folder_copy_and_push(parent_folder, source_folder, commit_message):
    """
    Copy a folder into all repositories, stage, commit, and push the changes.
    """
    # Loop through all directories in the parent folder
    for root, dirs, files in os.walk(parent_folder):
        for dir_name in dirs:
            repo_path = os.path.join(root, dir_name)
            try:
                # Copy the folder to the repository
                copy_folder_to_repos(source_folder, repo_path)

                # Stage, commit, and push the changes
                stage_commit_and_push(repo_path, commit_message)
            except Exception as e:
                print(f"Skipping {repo_path} due to errors.")
                print(f"Error: {e}")
        break# Prevent walking into subdirectories

    print("\n")

if __name__ == "__main__":
    os.system('clear')

    # Prompt the user for the parent folder path
    parent_folder = input("Enter the path to the folder containing your Git repositories: ").strip()
    parent_folder = os.path.abspath(parent_folder)
    
    # Validate the parent folder path
    if not os.path.isdir(parent_folder):
        print(f"The path '{parent_folder}' does not exist or is not a directory.")
        exit(1)
    
    # Prompt the user for the source folder path
    source_folder = input("Enter the path to the folder you want to copy into all repositories: ").strip()
    source_folder = os.path.abspath(source_folder)
    
    # Validate the source folder path
    if not os.path.isdir(source_folder):
        print(f"The path '{source_folder}' does not exist or is not a directory.")
        exit(1)
    
    # Prompt the user for the commit message
    commit_message = input("Enter the commit message to use for all repositories: ").strip()
    
    if not commit_message:
        print("Commit message cannot be empty!")
        exit(1)
    
    print_separator()

    # Run the automation
    automate_folder_copy_and_push(parent_folder, source_folder, commit_message)