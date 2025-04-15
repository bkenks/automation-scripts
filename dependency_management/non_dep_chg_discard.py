#!/usr/bin/env python3
import os
import subprocess
import sys
import argparse
import shutil
import tempfile

def discard_non_package_changes(parent_dir):
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

    for subdir in subdirs:
        full_path = os.path.join(parent_dir, subdir)
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
    return True

def main():
    parser = argparse.ArgumentParser(description='Discard all Git changes except package.json and package-lock.json.')
    parser.add_argument('--directory', help='Parent directory containing git repositories')
    args = parser.parse_args()

    print(f"Starting to process repositories in '{args.directory}'")

    success = discard_non_package_changes(args.directory)

    if success:
        print("\nOperation completed.")
    else:
        print("\nOperation failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
