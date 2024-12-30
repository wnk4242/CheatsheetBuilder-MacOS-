import os
import json
import sys
from pathlib import Path


NOTES_FILE = "notes.json"

def set_terminal_size(rows, cols):
    """Set the terminal window size."""
    if sys.platform.startswith('win'):
        os.system(f'mode con: cols={cols} lines={rows}')
    else:
        # ANSI escape sequence to set terminal size
        print(f"\033[8;{rows};{cols}t", end="")

# Example: Set terminal size to 30 rows and 100 columns
set_terminal_size(30, 100)

def clear_screen():
        print("\033[H\033[J", end="")  # ANSI escape codes to clear the screen and move to the top

def load_notes():
    """Load notes from a JSON file."""
    try:
        # Determine the base directory
        if getattr(sys, 'frozen', False):  # Check if running as a standalone app
            base_dir = Path(sys.executable).parent  # App directory for standalone
        else:
            base_dir = Path(__file__).parent  # Script directory for non-standalone

        # Define the path to the notes JSON file
        file_path = base_dir / "notes.json"

        if not file_path.exists():
            print(f"File {file_path} not found. Starting with an empty notes structure.")
            return {}

        # Load the notes from the JSON file
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:
        print(f"Error loading notes: {e}")
        return {}

def save_notes(notes):
    """Save notes to a JSON file."""
    try:
        # Determine the base directory
        if getattr(sys, 'frozen', False):  # Check if running as a standalone app
            base_dir = Path(sys.executable).parent  # App directory for standalone
        else:
            base_dir = Path(__file__).parent  # Script directory for non-standalone

        # Define the path to the notes JSON file
        file_path = base_dir / "notes.json"

        # Save the notes to the JSON file
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(notes, f, indent=4)

    except Exception as e:
        print(f"Error saving notes: {e}")

