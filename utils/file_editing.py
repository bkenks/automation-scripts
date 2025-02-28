import os
import shutil

class FileEditing:
    @staticmethod
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