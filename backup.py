import os
import shutil
import sys
from datetime import datetime

def validate_directory(path):
    # Check if the folder is there or not
    if not os.path.exists(path):
        print(f"Error: Folder '{path}' is not found.")
        return False
    # Check if the given path is actually a folder
    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a folder.")
        return False
    return True

def generate_unique_filename(destination_dir, filename):
    # If the file is already there, we add time to the name to make it different
    base_name, extension = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{base_name}_{timestamp}{extension}"
    unique_path = os.path.join(destination_dir, unique_filename)

    # If the new name is also taken, we add more details
    while os.path.exists(unique_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        unique_filename = f"{base_name}_{timestamp}{extension}"
        unique_path = os.path.join(destination_dir, unique_filename)

    return unique_filename

def backup_files(source_dir, destination_dir):
    # Move files from one folder to another
    try:
        # Check if both folders exist
        if not validate_directory(source_dir):
            return
        if not validate_directory(destination_dir):
            return

        # Go through all files in the source folder
        for filename in os.listdir(source_dir):
            source_file = os.path.join(source_dir, filename)
            destination_file = os.path.join(destination_dir, filename)

            # Ignore folders, only take files
            if os.path.isdir(source_file):
                print(f"Skipping folder: {filename}")
                continue

            # If the file is already there, rename it with time
            if os.path.exists(destination_file):
                unique_filename = generate_unique_filename(destination_dir, filename)
                destination_file = os.path.join(destination_dir, unique_filename)
                print(f"File '{filename}' already exists. Renamed to '{unique_filename}'.")

            # Copy the file
            shutil.copy2(source_file, destination_file)
            print(f"Copied: {filename} -> {os.path.basename(destination_file)}")

        print("\nBackup done successfully.")

    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    # Check if user gave the right number of inputs
    if len(sys.argv) != 3:
        print("Use this: python backup.py <source_folder> <destination_folder>")
        sys.exit(1)

    # Get the folder names from the user input
    source_directory = sys.argv[1]
    destination_directory = sys.argv[2]

    # Start copying the files
    backup_files(source_directory, destination_directory)
