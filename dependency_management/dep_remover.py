#!/usr/bin/env python3
import os
import subprocess
import sys
import argparse
import json

def run_commands_in_subdirs(parent_dir, dependency):
    """
    Runs commands to remove a specified NPM dependency in each subdirectory,
    but only if the dependency exists in that project.
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
    
    processed_count = 0
    skipped_count = 0
    
    # Process each subdirectory
    for subdir in subdirs:
        full_path = os.path.join(parent_dir, subdir)
        package_json_path = os.path.join(full_path, 'package.json')
        
        # Check if it's an NPM project and if the dependency exists
        if not os.path.exists(package_json_path):
            print(f"\nSkipping {full_path} - Not an NPM project (no package.json)")
            skipped_count += 1
            continue
        
        # Check if dependency exists in the project
        try:
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
                
            dependency_exists = False
            
            # Check in dependencies
            if "dependencies" in package_data and dependency in package_data["dependencies"]:
                dependency_exists = True
            
            # Check in devDependencies
            if "devDependencies" in package_data and dependency in package_data["devDependencies"]:
                dependency_exists = True
                
            if not dependency_exists:
                print(f"\nSkipping {full_path} - Dependency '{dependency}' not found")
                skipped_count += 1
                continue
        except json.JSONDecodeError:
            print(f"\nSkipping {full_path} - Invalid package.json")
            skipped_count += 1
            continue
        except Exception as e:
            print(f"\nError checking {full_path}: {e}")
            skipped_count += 1
            continue
        
        print(f"\n{'='*50}")
        print(f"Processing directory: {full_path}")
        print(f"Removing dependency: {dependency}")
        print(f"{'='*50}")
        
        # Commands to run in the subdirectory
        commands = [
            f"npm uninstall {dependency}",
            "rm -rf node_modules package-lock.json",
            "npm run build",
            "npm install"
        ]
        
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
        processed_count += 1
    
    print(f"\nSummary: Processed {processed_count} directories, skipped {skipped_count} directories")
    return True

def main():
    parser = argparse.ArgumentParser(description='Remove an NPM dependency from all projects in subdirectories.')
    parser.add_argument('--directory', help='Parent directory containing projects')
    parser.add_argument('--dependency', help='NPM dependency to remove')
    args = parser.parse_args()
    
    print(f"Starting to process projects in '{args.directory}'")
    print(f"Will remove dependency '{args.dependency}' from all projects")
    
    success = run_commands_in_subdirs(args.directory, args.dependency)
    
    if success:
        print("\nOperation completed.")
    else:
        print("\nOperation failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()