"""
GitHub Pull Request Automation Script

This script automates the process of pushing a Git branch and creating a pull request (PR) 
for multiple Git repositories inside a specified parent folder. It performs the following tasks:

1. Iterates through all subdirectories of the given parent folder, assuming each is a
Git repository.
2. Pushes the specified branch to the remote repository.
3. Creates a pull request (PR) using the GitHub API.

Modules Required:
- os: For file system navigation.
- subprocess: For executing Git commands.
- requests: For making HTTP requests to the GitHub API.
- json: For handling API request payloads.

Functions:
- push_branch(repo_path): Pushes the current branch to the remote repository.
- create_pull_request(repo_path, branch_name, pr_title, pr_description, github_token):
  Creates a PR on GitHub for the specified branch.
- automate_pr_creation(parent_folder, branch_name, pr_title, pr_description, github_token):
  Automates branch pushing and PR creation for all repositories in a given parent folder.

Usage:
Run the script and provide the required inputs:
1. Parent folder containing Git repositories.
2. Branch name to push and create a PR for.
3. PR title and description.
4. GitHub Personal Access Token.

Example:
$ python automate_pr.py
Enter the path to the folder containing your Git repositories: /path/to/repos
Enter the name of the branch to push and create a PR for: feature-branch
Enter the title for the Pull Request: New Feature Implementation
Enter the description for the Pull Request: This PR adds a new feature.
Enter your GitHub Personal Access Token: <your_token_here>

Note:
- Ensure each subdirectory in the parent folder is a valid Git repository with a remote set up.
- The script assumes the base branch for the PR is "main." Modify it if needed.

Author: Brian Kenkel
"""

import os
import json
import subprocess
import requests

# GitHub API settings
GITHUB_API_URL = "https://api.github.com"

def print_separator():
    """
    Prints a separator line.
    """
    print("\n")
    print("----------")
    print("\n")

def push_branch(repo_path):
    """
    Push the current branch to the remote repository.
    """
    try:
        os.chdir(repo_path)
        subprocess.run(["git", "push", "origin", "HEAD"], check=True)
        print(f"Pushed branch in {repo_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error pushing branch in {repo_path}: {e}")
        raise

def create_pull_request(repo_path, branch_name, pr_title, pr_description, github_token):
    """
    Create a Pull Request using the GitHub API.
    """
    try:
        # Get the remote URL of the repository
        remote_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode().strip()
        
        # Extract owner and repo name from the remote URL
        if remote_url.startswith("https://github.com/"):
            # HTTPS URL format: https://github.com/owner/repo.git
            parts = remote_url[:-4].split("/")  # Remove .git and split
            owner, repo = parts[-2], parts[-1]
        elif remote_url.startswith("git@github.com:"):
            # SSH URL format: git@github.com:owner/repo.git
            parts = remote_url[:-4].split(":")  # Remove .git and split
            owner, repo = parts[-1].split("/")
        else:
            print(f"Skipping {repo_path}: Unsupported remote URL format.")
            return
        
        # GitHub API endpoint for creating a PR
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"
        
        # PR payload
        payload = {
            "title": pr_title,
            "head": branch_name,
            "base": "main",  # Change this to your base branch (e.g., "master")
            "body": pr_description
        }
        
        # Headers for authentication
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Make the API request
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 201:
            print(f"Created PR for branch '{branch_name}' in {repo_path}")
            print(f"PR URL: {response.json()['html_url']}")
        else:
            print(f"Failed to create PR for branch '{branch_name}' in {repo_path}")
            print(f"Response: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"Error creating PR in {repo_path}: {e}")

def automate_pr_creation(parent_folder, branch_name, pr_title, pr_description, github_token):
    """
    Automate PR creation for all Git repositories inside the parent folder.
    """
    # Loop through all directories in the parent folder
    for root, dirs, files in os.walk(parent_folder):
        for dir_name in dirs:
            repo_path = os.path.join(root, dir_name)
            try:
                # Push the branch
                push_branch(repo_path)
                
                # Create the PR
                create_pull_request(repo_path, branch_name, pr_title, pr_description, github_token)
            except Exception as e:
                print(f"Skipping {repo_path} due to the following errors.")
                print(f"Error: {e}")
            print("\n")
        break  # Prevent walking into subdirectories

if __name__ == "__main__":
    os.system('clear')

    # Prompt the user for the parent folder path
    parent_folder = input("Enter the path to the folder containing your Git repositories: ").strip()
    parent_folder = os.path.abspath(parent_folder)

    # Validate the path
    if not os.path.isdir(parent_folder):
        print(f"The path '{parent_folder}' does not exist or is not a directory.")
        exit(1)

    # Prompt the user for the branch name
    branch_name = input("Enter the name of the branch to push and create a PR for: ").strip()

    if not branch_name:
        print("Branch name cannot be empty!")
        exit(1)

    # Prompt the user for the PR title and description
    pr_title = input("Enter the title for the Pull Request: ").strip()
    pr_description = input("Enter the description for the Pull Request: ").strip()

    if not pr_title:
        print("PR title cannot be empty!")
        exit(1)

    # Prompt the user for the GitHub Personal Access Token
    github_token = input("Enter your GitHub Personal Access Token: ").strip()

    # Print a separator
    print_separator()

    if not github_token:
        print("GitHub Personal Access Token cannot be empty!")
        exit(1)

    # Run the automation
    automate_pr_creation(parent_folder, branch_name, pr_title, pr_description, github_token)
