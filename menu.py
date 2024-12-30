from options import cheatsheet_menu
from utils import clear_screen
from search import search_notes
from export import export_notes

def main_menu(notes):
    """Display the main menu and handle user input."""
    while True:
        clear_screen()
        print("\n[Cheatsheet Building System]")
        print()

        print("1. Cheatsheet Builder")
        print("2. Search Notes")
        print("3. Export Notes")
        print("4. Exit")

        print()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            cheatsheet_menu("[Main Menu]", notes["r_cheatsheet"], notes)
        elif choice == "2":
            search_notes(notes)
        elif choice == "3":
            export_notes(notes)
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")
