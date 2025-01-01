from utils import clear_screen, load_notes, save_notes, choose_notes_file
from options import cheatsheet_menu
from notes_operations import export_notes

def main_menu():
    """Display the main menu and handle user input."""
    notes = None
    selected_file = None

    while True:
        clear_screen()
        print("\n[Cheatsheet Building System]")
        print()
        print("1. New Cheatsheet")
        print("2. Load Cheatsheet")
        print("3. Export Cheatsheet")
        if selected_file:
            print("4. Reopen Current Cheatsheet")
        print("0. Exit")
        print()

        # Display the currently loaded cheatsheet if available
        if selected_file:
            print(f"Currently loaded cheatsheet: {selected_file}")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":  # New Cheatsheet
            selected_file = input("Enter a name for the new cheatsheet (without .json): ").strip() + ".json"
            if not selected_file.endswith(".json"):
                selected_file += ".json"

            # Create a blank cheatsheet
            notes = {"r_cheatsheet": {}}
            save_notes(notes, selected_file)
            print(f"New cheatsheet '{selected_file}' created.")
            input("Press Enter to continue...")
            cheatsheet_menu("New Cheatsheet", notes["r_cheatsheet"], notes, selected_file)

        elif choice == "2":  # Load Cheatsheet
            selected_file = choose_notes_file()
            if not selected_file:
                print("No cheatsheet selected. Returning to the main menu.")
                input("Press Enter to continue...")
                continue

            notes = load_notes(selected_file)
            print(f"Loaded cheatsheet '{selected_file}'.")
            input("Press Enter to continue...")
            cheatsheet_menu("Cheatsheet", notes["r_cheatsheet"], notes, selected_file)

        elif choice == "3":  # Export Notes
            if notes is None or selected_file is None:
                print("No cheatsheet loaded. Please create or load a cheatsheet first.")
                input("Press Enter to continue...")
                continue
            export_notes(notes, selected_file)

        elif choice == "4" and selected_file:  # Reopen Current Cheatsheet
            print(f"Reopening cheatsheet '{selected_file}'.")
            input("Press Enter to continue...")
            cheatsheet_menu("Cheatsheet", notes["r_cheatsheet"], notes, selected_file)

        elif choice == "0":  # Exit
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")
