#!/usr/bin/env python3
import os
import subprocess
import sys
import argparse

def run_commands_in_subdirs(parent_dir):
    """
    Runs specified commands in each immediate subdirectory of the parent directory.
    """
    # Get all immediate subdirectories
    try:
        subdirs = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]
    except FileNotFoundError:
        print(f"Error: Directory '{parent_dir}' not found.")
        return False
    
    if not subdirs:
        print(f"No subdirectories found in '{parent_dir}'.")
        return False
    
    # Commands to run in each subdirectory
    commands = [
        "rm -rf node_modules package-lock.json",
        "npm run build",
        "npm install"
    ]
    
    # Process each subdirectory
    for subdir in subdirs:
        full_path = os.path.join(parent_dir, subdir)
        print(f"\n{'='*50}")
        print(f"Processing directory: {full_path}")
        print(f"{'='*50}")
        
        # Change to the subdirectory
        original_dir = os.getcwd()
        os.chdir(full_path)
        
        # Run each command
        for cmd in commands:
            print(f"\nExecuting: {cmd}")
            try:
                process = subprocess.run(cmd, shell=True, check=False, text=True, 
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Print command output
                if process.stdout:
                    print("Output:")
                    print(process.stdout)
                
                # Print any errors
                if process.stderr:
                    print("Errors:")
                    print(process.stderr)
                
                if process.returncode != 0:
                    print(f"Warning: Command exited with code {process.returncode}")
            except Exception as e:
                print(f"Error executing command: {e}")
        
        # Return to original directory
        os.chdir(original_dir)
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Run Node.js commands in all subdirectories of a specified directory.')
    parser.add_argument('--directory', help='Parent directory containing subdirectories to process')
    args = parser.parse_args()
    
    print(f"Starting to process subdirectories in '{args.directory}'")
    success = run_commands_in_subdirs(args.directory)
    
    if success:
        print("\nAll directories processed.")
    else:
        print("\nOperation failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()