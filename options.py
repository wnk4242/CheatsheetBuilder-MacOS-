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

    # Extract the cheatsheet name from the file name
    cheatsheet_name = file_name.replace(".json", "")

    # Initialize breadcrumb if not passed
    if breadcrumb is None:
        breadcrumb = ["Main Menu"]

    while True:
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
        truncation_length = 20  # Set globally for easier adjustments
        if truncated_display:
            current_notes = [
                (note[:truncation_length] + "...") if len(note) > truncation_length else note for note in current_notes
            ]

        # Fetch folders
        folders = section.get("submenus", {})
        folder_keys = list(folders.keys())

        # Display notes and folders separately with a blank space
        notes_display = ([f"Notes (Page {page + 1} of {total_pages}):"] +
                         [f"- {note}" for note in current_notes]) if current_notes else ["Notes: No notes available."]
        folders_display = ["", "Folders:"] + [
            f"{i + 1}. {folder.replace('_', ' ').title()}" for i, folder in enumerate(folder_keys)
        ] if folders else ["", "Folders: No folders available."]

        # Combine for display
        right_side_display = notes_display + folders_display

        # Options with dynamic modes
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

        # Pagination options
        if page > 0:
            options.append("; Previous Page")
        if page < total_pages - 1:
            options.append("' Next Page")

        # Display both columns
        max_lines = max(len(options), len(right_side_display))
        for i in range(max_lines):
            left = options[i] if i < len(options) else ""
            right = right_side_display[i] if i < len(right_side_display) else ""
            print(f"{left:<35} | {right:<50}")

        # Get user input
        choice = input("\nEnter your choice: ").strip()

        if choice.lower() == 'a':
            add_note(section, notes, file_name)
        elif choice.lower() == 's':
            edit_note(section, notes, file_name)
        elif choice.lower() == 'd':
            delete_notes(section, notes, file_name)
        elif choice.lower() == 'j':
            add_folder(section.setdefault("submenus", {}), notes, file_name)
        elif choice.lower() == 'k':
            edit_folder(section.get("submenus", {}), notes, file_name)
        elif choice.lower() == 'l':
            delete_folders(section.get("submenus", {}), notes, file_name)
        elif choice.lower() == 'f':
            move_notes_to_folder(section, parent_section, notes, file_name)
        elif choice.lower() == 'n':
            move_folders_to_folder(section.get("submenus", {}), parent_section, notes, file_name)
        elif choice.lower() == 'm':
            arrange_folders_order(section.get("submenus", {}), notes, file_name)
        elif choice.lower() == 'q':
            alphabetical_order = not alphabetical_order
            print(f"Order toggled to {'Alphabetical' if alphabetical_order else 'Original'}.")
            input("Press Enter to continue...")
        elif choice.lower() == 'w':
            truncated_display = not truncated_display
            print(f"Note display toggled to {'Truncated' if truncated_display else 'Full'}.")
            input("Press Enter to continue...")
        elif choice.lower() == 'r':  # Search Notes
            search_notes(notes)
        elif choice == ";":
            if page > 0:
                page -= 1
        elif choice == "'":
            if page < total_pages - 1:
                page += 1
        elif choice == "e":
            return
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(folder_keys):
                folder_key = folder_keys[idx]
                cheatsheet_menu(
                    folder_key.replace('_', ' ').title(),
                    folders[folder_key],
                    notes,
                    file_name,
                    parent_section=section,
                    breadcrumb=breadcrumb + [folder_key.replace('_', ' ').title()]
                )
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")
