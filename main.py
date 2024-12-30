from menu import main_menu
from utils import load_notes

if __name__ == "__main__":
    # Load notes and start the main menu
    notes = load_notes()
    main_menu(notes)
