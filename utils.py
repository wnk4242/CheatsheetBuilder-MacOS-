import os
import sys
import json
from pathlib import Path

NOTES_FILE = "notes.json"

def set_terminal_size(rows, cols):
    """Set the terminal window size."""
    print(f"\033[8;{rows};{cols}t", end="")

# Example: Set terminal size to 30 rows and 100 columns
set_terminal_size(30, 100)

def clear_screen():
    print("\033[H\033[J", end="")  # ANSI escape codes to clear the screen and move to the top

def adjust_working_directory():
    """Adjust the working directory to the folder containing the app or script."""
    try:
        if getattr(sys, 'frozen', False):  # If running as a standalone app
            base_dir = Path(sys.executable).parent
        else:  # If running as a script
            base_dir = Path(__file__).parent

        os.chdir(base_dir)  # Change the working directory
    except Exception as e:
        print(f"Error adjusting working directory: {e}")

# Adjust the working directory at the start of the program
adjust_working_directory()

def choose_notes_file():
    """Allow the user to choose a JSON file for the notes."""
    files = list_json_files()
    if not files:
        print("No JSON files found in the current directory.")
        input("Press Enter to continue...")
        return None

    print("\nAvailable JSON files:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

    choice = input("\nEnter the number of the file you want to load: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(files):
        return files[int(choice) - 1]
    else:
        print("Invalid choice. Please select a valid number to open a cheatsheet.")
        return None

def load_notes(file_name=None):
    """Load notes from the specified JSON file."""
    try:
        # Determine the base directory
        if getattr(sys, 'frozen', False):  # Check if running as a standalone app
            base_dir = Path(sys.executable).parent  # App directory for standalone
        else:
            base_dir = Path(__file__).parent  # Script directory for non-standalone

        # Use the provided file name or default to NOTES_FILE
        file_path = base_dir / (file_name if file_name else NOTES_FILE)

        if not file_path.exists():
            print(f"File {file_path} not found. Starting with an empty notes structure.")
            return {}

        # Load the notes from the JSON file
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:
        print(f"Error loading notes: {e}")
        return {}


def save_notes(notes, file_name=None):
    """Save notes to a JSON file."""
    try:
        # Determine the base directory
        if getattr(sys, 'frozen', False):  # Check if running as a standalone app
            base_dir = Path(sys.executable).parent  # App directory for standalone
        else:
            base_dir = Path(__file__).parent  # Script directory for non-standalone

        # Use the provided file name or default to NOTES_FILE
        file_path = base_dir / (file_name if file_name else NOTES_FILE)

        # Save the notes to the JSON file
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(notes, f, indent=4)

        print(f"Notes saved successfully to {file_path}.")
    except Exception as e:
        print(f"Error saving notes: {e}")


def list_json_files():
    """List all available JSON files in the current directory."""
    return [f for f in os.listdir() if f.endswith(".json")]


