from utils import clear_screen
from notes_operations import (
    add_note,
    edit_note,
    delete_notes,
    move_notes_to_folder,
    add_folder,
    edit_folder,
    delete_folders,
    move_folders_to_folder,
    arrange_folders_order,
    search_notes,
)


def cheatsheet_menu(title, section, notes, file_name, parent_section=None, breadcrumb=None):
    """
    Display a menu for a specific section with pagination and toggleable options.
    Adds a dynamic breadcrumb navigation trail.
    """
    page = 0  # Start on the first page
    notes_per_page = 5  # Notes per page
    alphabetical_order = False  # Default to original order
    truncated_display = True  # Default to truncated note display
    show_options = True  # Track if the options menu is visible

    # Extract the cheatsheet name from the file name
    cheatsheet_name = file_name.replace(".json", "")

    # Initialize breadcrumb if not passed
    if breadcrumb is None:
        breadcrumb = ["Main Menu"]

    while True:
        try:
            clear_screen()

            # Display the cheatsheet name and breadcrumb navigation
            print(f"\nCheatsheet: {cheatsheet_name}\n")
            print(f"{' > '.join(breadcrumb)}\n")

            # Fetch notes and apply ordering if needed
            notes_list = section.get("notes", [])
            if alphabetical_order:
                notes_list = sorted(notes_list)

            # Pagination for notes
            total_pages = max(1, (len(notes_list) + notes_per_page - 1) // notes_per_page)
            start_idx = page * notes_per_page
            end_idx = start_idx + notes_per_page
            current_notes = notes_list[start_idx:end_idx]

            # Apply truncation if enabled
            truncation_length = 50  # Set globally for easier adjustments
            if truncated_display:
                current_notes = [
                    (note[:truncation_length] + "...") if len(note) > truncation_length else note for note in current_notes
                ]

            # Fetch folders
            folders = section.get("submenus", {})

            # Display notes only if available
            if current_notes:
                notes_display = [f"Notes (Page {page + 1} of {total_pages}):"] + [
                    f"- {note}" for note in current_notes
                ]
            else:
                notes_display = []

            # Display folders only if available
            if folders:
                folder_section = ["", "Folders:"] + [
                    f"{i + 1}. {folder.replace('_', ' ').title()}" for i, folder in enumerate(folders.keys())
                ]
            else:
                folder_section = []

            # Combine notes and folders for display
            display = notes_display + folder_section

            # Show options menu if toggled on
            if show_options:
                options = [
                    "a. Add Note",
                    "j. Add Folder",
                    "s. Edit Note",
                    "k. Edit Folder",
                    "d. Delete Notes",
                    "l. Delete Folders",
                    "f. Move Notes to Folder",
                    "n. Move Folders to Folder",
                    "m. Arrange Folders Order",
                    f"q. Toggle Note Order ({'Alphabetical' if alphabetical_order else 'Original'})",
                    f"w. Toggle Note Display ({'Truncated' if truncated_display else 'Full'})",
                    "r. Search Notes",
                    "e. Go Back",
                ]

                if page > 0:
                    options.append("; Previous Page")
                if page < total_pages - 1:
                    options.append("' Next Page")

                for i in range(max(len(options), len(display))):
                    left = options[i] if i < len(options) else ""
                    right = display[i] if i < len(display) else ""
                    print(f"{left:<35} | {right}")
            else:
                # Show only notes and folders when options are hidden
                for line in display:
                    print(line)

            # Get user input
            choice = input("\nEnter your choice (or press 'b' to hide/show the options menu): ").strip().lower()

            if choice == "b":
                show_options = not show_options
            elif choice == "e":
                return
            elif choice in ("a", "j", "s", "k", "d", "l", "f", "n", "m", "q", "w", "r", ";", "'"):
                if choice == "a":
                    add_note(section, notes, file_name)
                elif choice == "j":
                    add_folder(folders, notes, file_name)
                elif choice == "s":
                    edit_note(section, notes, file_name)
                elif choice == "k":
                    edit_folder(folders, notes, file_name)
                elif choice == "d":
                    delete_notes(section, notes, file_name)
                elif choice == "l":
                    delete_folders(folders, notes, file_name)
                elif choice == "f":
                    move_notes_to_folder(section, parent_section, notes, file_name)
                elif choice == "n":
                    move_folders_to_folder(folders, parent_section, notes, file_name)
                elif choice == "m":
                    arrange_folders_order(folders, notes, file_name)
                elif choice == "q":
                    alphabetical_order = not alphabetical_order
                elif choice == "w":
                    truncated_display = not truncated_display
                elif choice == "r":
                    search_notes(notes)
                elif choice == ";":
                    if page > 0:
                        page -= 1
                elif choice == "'":
                    if page < total_pages - 1:
                        page += 1
            elif choice.isdigit() and 1 <= int(choice) <= len(folders):
                folder_idx = int(choice) - 1
                folder_key = list(folders.keys())[folder_idx]
                cheatsheet_menu(
                    folder_key.replace("_", " ").title(),
                    folders[folder_key],
                    notes,
                    file_name,
                    parent_section=section,
                    breadcrumb=breadcrumb + [folder_key.replace("_", " ").title()],
                )
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
        except Exception as e:
            print(f"Error: {e}")
            input("Press Enter to continue...")
