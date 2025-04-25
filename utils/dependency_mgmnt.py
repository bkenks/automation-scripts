#!/usr/bin/env python3
import os
import subprocess
import sys
import argparse
import json
import shutil
import tempfile
from collections import Counter

class Dependency_MGMNT:
    def discard_non_package_changes(parent_repo_path):
        print(f"Starting to process repositories in '{parent_repo_path}'")

        try:
            subdirs = [d for d in os.listdir(parent_repo_path) if os.path.isdir(os.path.join(parent_repo_path, d))]
        except FileNotFoundError:
            print(f"Error: Directory '{parent_repo_path}' not found.")
            print("\nOperation failed.")
            sys.exit(1)

        if not subdirs:
            print(f"No subdirectories found in '{parent_repo_path}'.")
            print("\nOperation failed.")
            sys.exit(1)

        processed_count = 0
        skipped_count = 0

        for subdir in subdirs:
            full_path = os.path.join(parent_repo_path, subdir)
            git_dir = os.path.join(full_path, '.git')

            if not os.path.exists(git_dir):
                print(f"\nSkipping {full_path} - Not a git repository")
                skipped_count += 1
                continue

            print(f"\n{'='*50}\nProcessing repository: {full_path}\n{'='*50}")
            original_dir = os.getcwd()
            os.chdir(full_path)

            temp_dir = tempfile.mkdtemp()
            package_files = ['package.json', 'package-lock.json']
            modified_files = []

            try:
                # Find modified files
                result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
                lines = result.stdout.strip().split('\n')

                for line in lines:
                    if not line:
                        continue
                    file_path = line[3:]  # skip the status symbols
                    if file_path in package_files:
                        if os.path.exists(file_path):
                            shutil.copy2(file_path, os.path.join(temp_dir, file_path))
                            modified_files.append(file_path)

                # Discard all changes
                subprocess.run(['git', 'reset', '--hard'], check=True)
                print("All changes discarded.")

                # Restore modified package files
                for file_name in modified_files:
                    backup_path = os.path.join(temp_dir, file_name)
                    if os.path.exists(backup_path):
                        shutil.copy2(backup_path, file_name)
                        print(f"Restored changes to {file_name}")

            except Exception as e:
                print(f"Error processing repository: {e}")
                skipped_count += 1

            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)
                os.chdir(original_dir)
                processed_count += 1

        print(f"\nSummary: Processed {processed_count} repositories, skipped {skipped_count} repositories")
        print("\nOperation completed.")

    def remove_dep(parent_repo_path, dependency):
        """
        Runs commands to remove a specified NPM dependency in each subdirectory,
        but only if the dependency exists in that project.
        """

        print(f"Starting to process projects in '{parent_repo_path}'")
        print(f"Will remove dependency '{dependency}' from all projects")

        # Get all immediate subdirectories
        try:
            subdirs = [d for d in os.listdir(parent_repo_path) if os.path.isdir(os.path.join(parent_repo_path, d))]
        except FileNotFoundError:
            print(f"Error: Directory '{parent_repo_path}' not found.")
            print("\nOperation failed.")
            sys.exit(1)
        
        if not subdirs:
            print(f"No subdirectories found in '{parent_repo_path}'.")
            print("\nOperation failed.")
            sys.exit(1)
        
        processed_count = 0
        skipped_count = 0
        
        # Process each subdirectory
        for subdir in subdirs:
            full_path = os.path.join(parent_repo_path, subdir)
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
        print("\nOperation completed.")

    def unused_dep_check(parent_repo_path):
        """
        Runs depcheck in each subdirectory and collects the results.
        """
        # Get all immediate subdirectories
        try:
            subdirs = [d for d in os.listdir(parent_repo_path) if os.path.isdir(os.path.join(parent_repo_path, d))]
        except FileNotFoundError:
            print(f"Error: Directory '{parent_repo_path}' not found.")
            print("\nAnalysis failed.")
            sys.exit(1)
        
        if not subdirs:
            print(f"No subdirectories found in '{parent_repo_path}'.")
            print("\nAnalysis failed.")
            sys.exit(1)
        
        processed_count = 0
        skipped_count = 0
        all_unused_deps = {}
        projects_with_dep = {}
        
        # Process each subdirectory
        for subdir in subdirs:
            full_path = os.path.join(parent_repo_path, subdir)
            package_json_path = os.path.join(full_path, 'package.json')
            
            # Check if it's an NPM project
            if not os.path.exists(package_json_path):
                print(f"\nSkipping {full_path} - Not an NPM project (no package.json)")
                skipped_count += 1
                continue
            
            print(f"\n{'='*50}")
            print(f"Running depcheck in: {full_path}")
            print(f"{'='*50}")
            
            # Change to the subdirectory
            original_dir = os.getcwd()
            os.chdir(full_path)
            
            # Run depcheck
            try:
                # First check if depcheck is installed
                check_depcheck = subprocess.run("which depcheck || npm list -g depcheck", shell=True, text=True, 
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Install depcheck locally if not found globally
                if "depcheck" not in check_depcheck.stdout:
                    print("Depcheck not found globally, installing it locally...")
                    install_depcheck = subprocess.run("npm install depcheck --no-save", shell=True, text=True,
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    depcheck_cmd = "NODE_OPTIONS=--no-deprecation npx depcheck --json"
                else:
                    depcheck_cmd = "NODE_OPTIONS=--no-deprecation depcheck --json"
                
                print(f"\nExecuting: {depcheck_cmd}")
                process = subprocess.run(depcheck_cmd, shell=True, check=False, text=True, 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Display warnings but don't treat them as failures
                if process.stderr:
                    print("Warnings (not affecting analysis):")
                    print(process.stderr)
                
                # Check if we got any JSON output
                if not process.stdout or not process.stdout.strip():
                    print(f"No output received from depcheck. Skipping {subdir}.")
                    os.chdir(original_dir)
                    skipped_count += 1
                    continue
                
                # Parse the JSON output
                try:
                    depcheck_result = json.loads(process.stdout)
                    
                    # Get unused dependencies
                    unused_deps = []
                    if 'dependencies' in depcheck_result:
                        unused_deps.extend(depcheck_result['dependencies'])
                    if 'devDependencies' in depcheck_result:
                        unused_deps.extend(depcheck_result['devDependencies'])
                    
                    print(f"Found {len(unused_deps)} unused dependencies in {subdir}")
                    
                    # Add to the overall collection
                    all_unused_deps[subdir] = unused_deps
                    
                    # Track which projects have which dependency
                    for dep in unused_deps:
                        if dep not in projects_with_dep:
                            projects_with_dep[dep] = []
                        projects_with_dep[dep].append(subdir)
                    
                except json.JSONDecodeError:
                    print(f"Failed to parse depcheck output. It may not be valid JSON.")
                    print(f"Output was: {process.stdout}")
                    skipped_count += 1
                    
            except Exception as e:
                print(f"Error running depcheck: {e}")
                skipped_count += 1
            
            # Return to original directory
            os.chdir(original_dir)
            processed_count += 1
        
        # Skip summary if no data collected
        if not all_unused_deps:
            print("\nNo usable data collected from any projects.")
            return True
        
        # Generate the summary report
        print(f"\n{'='*50}")
        print(f"SUMMARY REPORT")
        print(f"{'='*50}")
        print(f"Processed {processed_count} projects, skipped {skipped_count} projects")
        
        # Calculate overall stats
        all_unused = []
        for project, deps in all_unused_deps.items():
            all_unused.extend(deps)
        
        dependency_counts = Counter(all_unused)
        
        # Sort by frequency (most common first)
        common_unused = dependency_counts.most_common()
        
        print(f"\nUnused dependencies across all projects:")
        print(f"{'='*50}")
        print(f"{'Dependency':<40} {'Count':<8} {'Projects'}")
        print(f"{'-'*40} {'-'*8} {'-'*30}")
        
        for dep, count in common_unused:
            project_list = ', '.join(projects_with_dep[dep])
            if len(project_list) > 30:
                project_list = project_list[:27] + "..."
            print(f"{dep:<40} {count:<8} {project_list}")
        
        # Save results to a file
        result_file = os.path.join(parent_repo_path, "unused_dependencies_report.json")
        try:
            with open(result_file, 'w') as f:
                json.dump({
                    "summary": {
                        "processed": processed_count,
                        "skipped": skipped_count
                    },
                    "unused_by_project": all_unused_deps,
                    "projects_by_dependency": {dep: projs for dep, projs in projects_with_dep.items()}
                }, f, indent=2)
            print(f"\nDetailed report saved to: {result_file}")
        except Exception as e:
            print(f"Error saving report file: {e}")
        
        print("\nAnalysis completed.")