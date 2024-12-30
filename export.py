from pathlib import Path
import sys  # Ensure sys is imported


def export_notes(notes):
    """Export notes to a text file in the current project folder or alongside the app."""
    try:
        # Determine base directory relative to the app bundle
        if getattr(sys, 'frozen', False):  # Check if running as a standalone app
            base_dir = Path(sys.executable).parent  # For PyInstaller or similar bundling
        else:
            base_dir = Path(__file__).parent  # For running directly from the script

        # Define the file path for the export
        file_name = "notes_export.txt"
        file_path = base_dir / file_name

        # Write the notes to the export file
        with file_path.open("w", encoding="utf-8") as f:
            for key, value in notes.items():
                f.write(f"Section: {key}\n")
                f.write("Notes:\n")
                for note in value.get("notes", []):
                    f.write(f"- {note}\n")
                f.write("\n")

        print(f"Notes exported successfully to {file_path.resolve()}")
    except Exception as e:
        print(f"Error exporting notes: {e}")
