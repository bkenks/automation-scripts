#!/usr/bin/env python3
import os
import subprocess
import sys
import argparse
import json
from collections import Counter

def run_depcheck_in_subdirs(parent_dir):
    """
    Runs depcheck in each subdirectory and collects the results.
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
    all_unused_deps = {}
    projects_with_dep = {}
    
    # Process each subdirectory
    for subdir in subdirs:
        full_path = os.path.join(parent_dir, subdir)
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
    result_file = os.path.join(parent_dir, "unused_dependencies_report.json")
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
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Run depcheck on all projects in subdirectories and summarize unused dependencies.')
    parser.add_argument('directory', help='Parent directory containing projects')
    args = parser.parse_args()
    
    print(f"Starting depcheck analysis on projects in '{args.directory}'")
    
    success = run_depcheck_in_subdirs(args.directory)
    
    if success:
        print("\nAnalysis completed.")
    else:
        print("\nAnalysis failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()