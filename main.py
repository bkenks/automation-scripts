import os
from pick import pick
from utils import FileEditing, GitHubActions, Formatting

class MainApp:
    def __init__(self):
        """
        Initialize the main application.
        """
        os.system('clear')
        self.repo_path = None  # Folder containing all repositories
        self.utils = None  # Placeholder for your utility class

    # Set defaults
    def set_repo_path(self):
        """
        Prompt the user for the parent folder containing all repositories.
        """
        os.system('clear')

        self.repo_path = input("Enter the path to the folder containing your Git repositories: ").strip()
        self.repo_path = os.path.abspath(self.repo_path)
        
        # Validate the path
        if not os.path.isdir(self.repo_path):
            print(f"The path '{self.repo_path}' does not exist or is not a directory.")
            self.repo_path = None
    
    def get_user_pat(self):
        """
        Get the Github Personal Access Token
        """
        os.system('clear')
        # Prompt the user for the GitHub Personal Access Token
        self.github_token = input("Enter your GitHub Personal Access Token: ").strip()

        if not self.github_token:
            print("GitHub Personal Access Token cannot be empty!")
            exit(1)

    ##########################


    # Bulk Actions #
    def bulk_create_and_checkout_branches(self):
        """
        Bulk create and checkout branches in all repositories.
        """
        os.system('clear')

        if not self.repo_path:
            print("Parent folder not set. Please set the parent folder first.")
            input("\nPress Enter to go back to the menu...")
            return
        
        # Prompt the user for the new branch name
        branch_name = input("Enter the name of the new branch: ").strip()

        if not branch_name:
            print("Branch name cannot be empty!")
        else:
            Formatting.print_separator()
            # Loop through all directories in the parent folder
            for root, dirs, files in os.walk(self.repo_path):
                for dir_name in dirs:
                    repo_path = os.path.join(root, dir_name)
                    GitHubActions.create_and_switch_branch(repo_path, branch_name)
                    GitHubActions.push_branch_set_upstream(repo_path)
                    print("\n")
                break  # Prevent walking into subdirectories
        
        input("Press Enter to go back to the menu...")

    def bulk_delete_branches(self):
        """
        Bulk delete branches in all repositories.
        """
        os.system('clear')

        if not self.repo_path:
            print("Parent folder not set. Please set the parent folder first.")
            input("\nPress Enter to go back to the menu...")
            return
        
        branch_name = input("Enter the name of the branch to delete: ").strip()

        if not branch_name:
            print("Branch name cannot be empty!")
        else:
            Formatting.print_separator()
            for root, dirs, files in os.walk(self.repo_path):
                for dir_name in dirs:
                    repo_path = os.path.join(root, dir_name)
                    GitHubActions.delete_local_and_remote_branch(repo_path, branch_name)
                    print("\n")
                break  # Prevent walking into subdirectories
        
        input("Press Enter to go back to the menu...")
        
        # Example: Call your utility function here
        # branch_name = input("Enter the name of the branch to delete: ").strip()
        # self.utils.delete_branches(self.repo_path, branch_name)
        # print("Bulk delete branches functionality goes here.")

    def bulk_copy_folder(self):
        """
        Bulk copy a folder into all repositories.
        """
        os.system('clear')

        if not self.repo_path:
            print("Parent folder not set. Please set the parent folder first.")
            input("\nPress Enter to go back to the menu...")
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
        for root, dirs, files in os.walk(self.repo_path):
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
            break# Prevent walking into subdirectories

        input("Press Enter to go back to the menu...")

    def bulk_commit_and_push(self):
        """
        Bulk copy a folder into all repositories.
        """
        os.system('clear')

        if not self.repo_path:
            print("Parent folder not set. Please set the parent folder first.")
            input("\nPress Enter to go back to the menu...")
            return
        
        # Prompt the user for the commit message
        commit_message = input("Enter the commit message to use for all repositories: ").strip()
        
        if not commit_message:
            print("Commit message cannot be empty!")
            exit(1)
        
        Formatting.print_separator()

        # Loop through all directories in the parent folder
        for root, dirs, files in os.walk(self.repo_path):
            for dir_name in dirs:
                repo_path = os.path.join(root, dir_name)
                try:
                    # Stage, commit, and push the changes
                    GitHubActions.stage_commit_and_push(repo_path, commit_message)
                except Exception as e:
                    print(f"Skipping {repo_path} due to errors.")
                    print(f"Error: {e}")
            break# Prevent walking into subdirectories

        input("Press Enter to go back to the menu...")

    def bulk_revert_pkglck(self):
        """
        Bulk copy a folder into all repositories.
        """
        os.system('clear')

        if not self.repo_path:
            print("Parent folder not set. Please set the parent folder first.")
            input("\nPress Enter to go back to the menu...")
            return
        
        Formatting.print_separator()

        # Loop through all directories in the parent folder
        for root, dirs, files in os.walk(self.repo_path):
            for dir_name in dirs:
                repo_path = os.path.join(root, dir_name)
                try:
                    # Stage, commit, and push the changes
                    GitHubActions.revert_package_lock_to_master(repo_path)
                except Exception as e:
                    print(f"Skipping {repo_path} due to errors.")
                    print(f"Error: {e}")
                Formatting.print_separator()
            break# Prevent walking into subdirectories

        input("Press Enter to go back to the menu...")

    def bulk_create_enterprise_prs(self):
        """
        Bulk create PRs for all repositories.
        """
        os.system('clear')

        if not self.repo_path:
            print("Parent folder not set. Please set the parent folder first.")
            input("\nPress Enter to go back to the menu...")
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

        # Print a separator
        Formatting.print_separator()

        pr_links = []

        # Loop through all directories in the parent folder
        for root, dirs, files in os.walk(self.repo_path):
            for dir_name in dirs:
                repo_path = os.path.join(root, dir_name)
                try:
                    # Push the branch
                    GitHubActions.push_branch(repo_path)
                    
                    # Create the PR
                    pr_link = GitHubActions.create_pull_request_enterprise(repo_path, branch_name, pr_title, pr_description, self.github_token)

                    pr_links.append(f"{repo_path}: {pr_link}")

                    print("\n")
                except Exception as e:
                    print(f"Skipping {self.repo_path} due to the following errors.")
                    print(f"Error: {e}")
                Formatting.print_separator()
            break  # Prevent walking into subdirectories

        # Print all PR links at the end
        if pr_links:
            print("\nPull Request Links:")
            for link in pr_links:
                print(link)

        input("Press Enter to go back to the menu...")

    ##########################


    # Menu #
    def show_bulk_actions_menu(self):
        """
        Display the bulk actions menu and handle user input.
        """
        options = [
            "commit and push",
            "create then checkout branches",
            "delete branches",
            "copy folder into repositories",
            "create PRs",
            "back"
        ]

        while True:
            # Display the bulk actions menu
            selected_option, _ = pick(options, title="Select a bulk action:", indicator="=>")
            
            # Handle the selected option
            if selected_option == "commit and push":
                self.bulk_commit_and_push()
            elif selected_option == "create then checkout branches":
                self.bulk_create_and_checkout_branches()
            elif selected_option == "delete branches":
                self.bulk_delete_branches()
            elif selected_option == "copy folder into repositories":
                self.bulk_copy_folder()
            elif selected_option == "create PRs":
                self.bulk_create_enterprise_prs()
            elif selected_option == "back":
                break

    def show_menu(self):
        """
        Display the main menu and handle user input.
        """
        options = [
            "set defaults",
            "bulk actions",
            "exit"
        ]
        
        while True:
            # Display the main menu
            selected_option, _ = pick(options, title="Select an action:", indicator="=>")
            
            # Handle the selected option
            if selected_option == "set defaults":
                self.show_path_token_menu()
            elif selected_option == "bulk actions":
                self.show_bulk_actions_menu()
            if selected_option == "exit":
                print("Exiting the application. Goodbye!")
                break

    def show_path_token_menu(self):
        """
        Display the menu to set GitHub Token and path of GitHub Repos

        """
        options = [
            "set parent folder of repos",
            "set github personal access token",
            "back"
        ]
        
        while True:
            # Display the main menu
            selected_option, _ = pick(options, title="Select an action:\n[Both actions are required for all bulk actions]", indicator="=>")
            
            # Handle the selected option
            if selected_option == "set parent folder of repos":
                self.set_repo_path()
            if selected_option == "set github personal access token":
                self.get_user_pat()
            elif selected_option == "back":
                break

    #######


if __name__ == "__main__":
    # Initialize and run the application
    app = MainApp()
    app.show_menu()