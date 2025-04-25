import os
import json
import subprocess
import requests
from github import Github, Auth

GITHUB_API_URL = "https://github.info53.com"

class GitHubActions:
    @staticmethod
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

    @staticmethod
    def push_branch_set_upstream(repo_path):
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

    @staticmethod
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

    @staticmethod
    def delete_local_and_remote_branch(repo_path, branch_name):
        """
        Delete the specified branch locally and remotely in the given repository.
        If the branch is currently checked out, switch to 'master' (or 'main') before deletion.
        """
        try:
            # Navigate to the repository directory
            os.chdir(repo_path)

            # Check if the directory is a Git repository
            if not os.path.isdir(".git"):
                print(f"Skipping {repo_path}: Not a Git repository.")
                return

            # Get the current branch name
            result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], 
                                    capture_output=True, text=True, check=True)
            current_branch = result.stdout.strip()

            # If the current branch is the one to be deleted, switch to 'master' or 'main'
            if current_branch == branch_name:
                print(f"Currently on branch '{branch_name}', switching to 'master' or 'main' before deletion.")
                switch_branch = "master" if subprocess.run(["git", "show-ref", "--verify", "--quiet", "refs/heads/master"]).returncode == 0 else "main"
                subprocess.run(["git", "checkout", switch_branch], check=True)
                print(f"Switched to '{switch_branch}'.")

            # Delete the local branch
            subprocess.run(["git", "branch", "-D", branch_name], check=True)
            print(f"Deleted local branch '{branch_name}' in {repo_path}")

            # Delete the remote branch
            subprocess.run(["git", "push", "origin", "--delete", branch_name], check=True)
            print(f"Deleted remote branch '{branch_name}' in {repo_path}")

        except subprocess.CalledProcessError as e:
            print(f"Error in {repo_path}: {e}")
        except Exception as e:
            print(f"Unexpected error in {repo_path}: {e}")

    @staticmethod
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

    # @staticmethod
    # def create_pull_request(repo_path, branch_name, pr_title, pr_description, github_token):
    #     """
    #     Create a Pull Request using the GitHub API.
    #     """
    #     try:
    #         # Get the remote URL of the repository
    #         remote_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode().strip()
            
    #         # Extract owner and repo name from the remote URL
    #         if remote_url.startswith("https://github.com/"):
    #             # HTTPS URL format: https://github.com/owner/repo.git
    #             parts = remote_url[:-4].split("/")  # Remove .git and split
    #             owner, repo = parts[-2], parts[-1]
    #         elif remote_url.startswith("git@github.com:"):
    #             # SSH URL format: git@github.com:owner/repo.git
    #             parts = remote_url[:-4].split(":")  # Remove .git and split
    #             owner, repo = parts[-1].split("/")
    #         else:
    #             print(f"Skipping {repo_path}: Unsupported remote URL format.")
    #             return
            
    #         # GitHub API endpoint for creating a PR
    #         url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"
            
    #         # PR payload
    #         payload = {
    #             "title": pr_title,
    #             "head": branch_name,
    #             "base": "main",  # Change this to your base branch (e.g., "master")
    #             "body": pr_description
    #         }
            
    #         # Headers for authentication
    #         headers = {
    #             "Authorization": f"token {github_token}",
    #             "Accept": "application/vnd.github.v3+json"
    #         }
            
    #         # Make the API request
    #         response = requests.post(url, headers=headers, data=json.dumps(payload))
            
    #         if response.status_code == 201:
    #             print(f"Created PR for branch '{branch_name}' in {repo_path}")
    #             print(f"PR URL: {response.json()['html_url']}")
    #         else:
    #             print(f"Failed to create PR for branch '{branch_name}' in {repo_path}")
    #             print(f"Response: {response.status_code} - {response.text}")
        
    #     except Exception as e:
    #         print(f"Error creating PR in {repo_path}: {e}")

    @staticmethod
    def create_pull_request_enterprise(repo_path, branch_name, pr_title, pr_description, github_token):
        """
        Create a Pull Request using the PyGithub library for GitHub Enterprise.
        """
        try:
            # Get the remote URL of the repository
            remote_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode().strip()
            
            # Extract owner and repo name from the remote URL
            if remote_url.startswith(GITHUB_API_URL):
                # HTTPS URL format: https://GITHUB_API_URL/owner/repo.git
                parts = remote_url[len(GITHUB_API_URL):].strip("/").split("/")  # Remove base URL and split
                owner, repo = parts[-2], parts[-1][:-4]  # Remove .git from repo name
            elif remote_url.startswith(f"git@{GITHUB_API_URL.split('//')[1]}:"):
                # SSH URL format: git@GITHUB_API_URL:owner/repo.git
                parts = remote_url.split(":")[-1].split("/")  # Extract owner and repo
                owner, repo = parts[-2], parts[-1][:-4]  # Remove .git from repo name
            else:
                print(f"Skipping {repo_path}: Unsupported remote URL format.")
                return
            
            # Authenticate with GitHub Enterprise
            auth = Auth.Token(github_token)
            g = Github(base_url=f"{GITHUB_API_URL}/api/v3", auth=auth)
            
            # Get the repository object
            repository = g.get_repo(f"{owner}/{repo}")
            
            # Create the pull request
            pr = repository.create_pull(
                title=pr_title,
                body=pr_description,
                head=branch_name,
                base="master"  # Change this to your base branch (e.g., "master")
            )
            
            print(f"Created PR for branch '{branch_name}' in {repo_path}")
            print(f"PR URL: {pr.html_url}")
        
        except Exception as e:
            print(f"Error creating PR in {repo_path}: {e}")

    @staticmethod
    def revert_package_lock_to_master(repo_path):
        """
        Revert the 'package-lock.json' file to the version in the 'master' branch.
        """
        try:
            # Navigate to the repository directory
            os.chdir(repo_path)

            # Check if the directory is a Git repository
            if not os.path.isdir(".git"):
                print(f"Skipping {repo_path}: Not a Git repository.")
                return

            # Check if 'package-lock.json' exists in the repository
            if not os.path.isfile("package-lock.json"):
                print(f"Skipping {repo_path}: 'package-lock.json' not found.")
                return

            # Fetch the latest changes from the remote
            subprocess.run(["git", "fetch", "origin"], check=True)

            # Revert 'package-lock.json' to the version in 'master'
            subprocess.run(["git", "checkout", "origin/master", "--", "package-lock.json"], check=True)
            print(f"Reverted 'package-lock.json' to 'master' version in {repo_path}")

        except subprocess.CalledProcessError as e:
            print(f"Error in {repo_path}: {e}")
        except Exception as e:
            print(f"Unexpected error in {repo_path}: {e}")