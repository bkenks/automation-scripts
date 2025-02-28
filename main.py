import os
from utils import FileEditing, GitHubActions, Formatting
from pick import pick  # For interactive menu

class MainApp:
    def __init__(self):
        """
        Initialize the main application.
        """
        os.system('clear')
        self.repo_path = None  # Folder containing all repositories
        self.utils = None  # Placeholder for your utility class

    def set_repo_path(self):
        """
        Prompt the user for the parent folder containing all repositories.
        """
        self.repo_path = input("Enter the path to the folder containing your Git repositories: ").strip()
        self.repo_path = os.path.abspath(self.repo_path)
        
        # Validate the path
        if not os.path.isdir(self.repo_path):
            print(f"The path '{self.repo_path}' does not exist or is not a directory.")
            self.repo_path = None

    def bulk_create_and_checkout_branches(self):
        """
        Bulk create and checkout branches in all repositories.
        """
        if not self.repo_path:
            print("Parent folder not set. Please set the parent folder first.")
            return
        
        # Prompt the user for the new branch name
        branch_name = input("Enter the name of the new branch: ").strip()

        if not branch_name:
            print("Branch name cannot be empty!")
        else:
            Formatting.print_separator()
            # Loop through all directories in the parent folder
            for root, dirs, files in os.walk(repo_path):
                for dir_name in dirs:
                    repo_path = os.path.join(root, dir_name)
                    GitHubActions.create_and_switch_branch(self.repo_path, "main")
                    GitHubActions.push_branch(self.repo_path)
                break  # Prevent walking into subdirectories

        print("\n")

    def bulk_delete_branches(self):
        """
        Bulk delete branches in all repositories.
        """
        if not self.repo_path:
            print("Parent folder not set. Please set the parent folder first.")
            return
        
        branch_name = input("Enter the name of the branch to delete: ").strip()

        if not branch_name:
            print("Branch name cannot be empty!")
        else:
            Formatting.print_separator()
            for root, dirs, files in os.walk(repo_path):
                for dir_name in dirs:
                    repo_path = os.path.join(root, dir_name)
                    GitHubActions.delete_local_and_remote_branch(repo_path, branch_name)
                break  # Prevent walking into subdirectories
        
        # Example: Call your utility function here
        # branch_name = input("Enter the name of the branch to delete: ").strip()
        # self.utils.delete_branches(self.repo_path, branch_name)
        # print("Bulk delete branches functionality goes here.")

    def bulk_copy_folder(self):
        """
        Bulk copy a folder into all repositories.
        """
        if not self.repo_path:
            print("Parent folder not set. Please set the parent folder first.")
            return
        
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
        
        Formatting.print_separator()

        # Loop through all directories in the parent folder
        for root, dirs, files in os.walk(repo_path):
            for dir_name in dirs:
                repo_path = os.path.join(root, dir_name)
                try:
                    # Copy the folder to the repository
                    FileEditing.copy_folder_to_repos(source_folder, repo_path)

                    # Stage, commit, and push the changes
                    GitHubActions.stage_commit_and_push(repo_path, commit_message)
                except Exception as e:
                    print(f"Skipping {repo_path} due to errors.")
                    print(f"Error: {e}")
            break # Prevent walking into subdirectories

        # Example: Call your utility function here
        # source_folder = input("Enter the path to the folder you want to copy: ").strip()
        # commit_message = input("Enter the commit message: ").strip()
        # self.utils.copy_folder_to_repos(self.repo_path, source_folder, commit_message)
        # print("Bulk copy folder functionality goes here.")

    def bulk_create_prs(self):
        """
        Bulk create PRs for all repositories.
        """
        if not self.repo_path:
            print("Parent folder not set. Please set the parent folder first.")
            return
        
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

        if not github_token:
            print("GitHub Personal Access Token cannot be empty!")
            exit(1)

        # Print a separator
        Formatting.print_separator()

        # Loop through all directories in the parent folder
        for root, dirs, files in os.walk(repo_path):
            for dir_name in dirs:
                repo_path = os.path.join(root, dir_name)
                try:
                    # Push the branch
                    GitHubActions.push_branch(repo_path)
                    
                    # Create the PR
                    GitHubActions.create_pull_request(repo_path, branch_name, pr_title, pr_description, github_token)
                except Exception as e:
                    print(f"Skipping {repo_path} due to the following errors.")
                    print(f"Error: {e}")
                print("\n")
            break  # Prevent walking into subdirectories
        
        # Example: Call your utility function here
        # branch_name = input("Enter the name of the branch to create PRs for: ").strip()
        # pr_title = input("Enter the PR title: ").strip()
        # pr_description = input("Enter the PR description: ").strip()
        # self.utils.create_prs(self.repo_path, branch_name, pr_title, pr_description)
        print("Bulk create PRs functionality goes here.")

    def show_bulk_actions_menu(self):
        """
        Display the submenu for bulk GitHub actions.
        """
        bulk_options = [
            "Bulk create and checkout branches",
            "Bulk delete branches",
            "Bulk copy folder into repositories",
            "Bulk create PRs",
            "Return to main menu"
        ]
        
        while True:
            # Display the submenu
            selected_option, _ = pick(bulk_options, title="Select a bulk action:", indicator="=>")
            
            # Handle the selected option
            if selected_option == "Bulk create and checkout branches":
                self.bulk_create_and_checkout_branches()
            elif selected_option == "Bulk delete branches":
                self.bulk_delete_branches()
            elif selected_option == "Bulk copy folder into repositories":
                self.bulk_copy_folder()
            elif selected_option == "Bulk create PRs":
                self.bulk_create_prs()
            elif selected_option == "Return to main menu":
                break

    def show_menu(self):
        """
        Display the main interactive menu and handle user input.
        """
        main_options = [
            "Set parent folder (required for all actions)",
            "Bulk GitHub Actions",
            "Exit"
        ]
        
        while True:
            # Display the main menu
            selected_option, _ = pick(main_options, title="Select an action:", indicator="=>")
            
            # Handle the selected option
            if selected_option == "Set parent folder (required for all actions)":
                self.set_parent_folder()
            elif selected_option == "Bulk GitHub Actions":
                self.show_bulk_actions_menu()
            elif selected_option == "Exit":
                print("Exiting the application. Goodbye!")
                break

if __name__ == "__main__":
    # Initialize and run the application
    app = MainApp()
    app.show_menu()