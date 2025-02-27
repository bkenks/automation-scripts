import os
import subprocess

def print_separator():
    """
    Prints a separator line.
    """
    print("\n")
    print("----------")
    print("\n")

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

def automate_branch_deletion(parent_folder, branch_name):
    """
    Automate branch deletion in all Git repositories inside the parent folder.
    """
    # Loop through all directories in the parent folder
    for root, dirs, files in os.walk(parent_folder):
        for dir_name in dirs:
            repo_path = os.path.join(root, dir_name)
            delete_local_and_remote_branch(repo_path, branch_name)
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

    # Prompt the user for the branch name to delete
    branch_name = input("Enter the name of the branch to delete: ").strip()

    if not branch_name:
        print("Branch name cannot be empty!")
    else:
        print_separator()
        automate_branch_deletion(parent_folder, branch_name)