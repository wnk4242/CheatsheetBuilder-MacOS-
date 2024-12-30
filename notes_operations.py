from utils import save_notes

def add_note(section, notes):
    """Add a new note to the section."""
    note = input("Enter the new note (or press Enter to cancel): ").strip()
    if not note:
        print("No note added. Returning to the menu.")
        input("Press Enter to continue...")
        return
    section.setdefault("notes", []).append(note)
    save_notes(notes)
    print("Note added successfully.")
    input("Press Enter to continue...")




def edit_note(section, notes):
    """Edit an existing note in the section."""
    notes_list = section.get("notes", [])
    if not notes_list:
        print("No notes to edit.")
        input("Press Enter to return to the menu...")
        return

    print("Available Notes:")
    for i, note in enumerate(notes_list, 1):
        print(f"{i}. {note}")

    choice = input("Enter the note number to edit (or press Enter to cancel): ").strip()

    if not choice:  # If the user presses Enter without input
        print("No edits made. Returning to the menu.")
        input("Press Enter to continue...")
        return

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(notes_list):
            print(f"Current note: {notes_list[idx]}")
            new_note = input("Enter the new note (or press Enter to cancel): ").strip()
            if not new_note:
                print("No changes made. Returning to the menu.")
                input("Press Enter to continue...")
                return
            notes_list[idx] = new_note
            save_notes(notes)
            print("Note updated successfully!")
        else:
            print("Invalid note number. Returning to the menu.")
    else:
        print("Invalid input. Returning to the menu.")

    input("Press Enter to continue...")


def delete_notes(section, notes):
    """Delete multiple notes from the section."""
    notes_list = section.get("notes", [])
    if not notes_list:
        print("No notes to delete.")
        input("Press Enter to continue...")
        return

    # Display available notes
    print("Available Notes:")
    for i, note in enumerate(notes_list, 1):
        print(f"{i}. {note}")

    #print("\nType 'all' to delete all notes.")
    # Prompt user for note numbers to delete
    selected = input(
        "Enter the note numbers to delete (comma-separated, 'all' to delete all notes, or press Enter to cancel): "
    ).strip()

    if not selected:
        print("No notes selected. Returning to menu.")
        input("Press Enter to continue...")
        return

    if selected.lower() == "all":
        confirm = input("Are you sure you want to delete all notes? (y/n): ").strip().lower()
        if confirm == "y":
            notes_list.clear()
            save_notes(notes)
            print("All notes deleted successfully.")
        else:
            print("Delete all notes canceled.")
        input("Press Enter to continue...")
        return

    try:
        # Validate that all inputs are numeric
        indices = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]
        if not indices:
            raise ValueError  # No valid numbers were entered

        # Validate that indices are within range
        invalid_indices = [idx for idx in indices if not (0 <= idx < len(notes_list))]
        if invalid_indices:
            print(f"Invalid note numbers: {', '.join(str(idx + 1) for idx in invalid_indices)}. No notes deleted.")
            input("Press Enter to continue...")
            return

        # Delete valid notes
        for idx in sorted(set(indices), reverse=True):  # Remove duplicates and sort descending
            notes_list.pop(idx)

        save_notes(notes)
        print("Selected notes deleted successfully.")
    except ValueError:
        print("Invalid input. No notes deleted.")
    input("Press Enter to continue...")

def move_notes_to_folder(current_section, parent_section, notes):
    """Move multiple notes from the current section into a specified folder."""
    notes_list = current_section.get("notes", [])
    if not notes_list:
        print("No notes available to move.")
        input("Press Enter to continue...")
        return

    # Display available notes
    print("Available Notes:")
    for i, note in enumerate(notes_list, 1):
        print(f"{i}. {note}")

    # Prompt user for note numbers to move
    selected = input(
        "Enter the note numbers to move (comma-separated, 'all' to move all notes, or press Enter to cancel): "
    ).strip()

    if not selected:
        print("No notes selected. Returning to menu.")
        input("Press Enter to continue...")
        return

    if selected.lower() == "all":
        indices = list(range(len(notes_list)))  # Select all notes
    else:
        try:
            indices = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]
            indices = sorted(set(indices), reverse=True)  # Remove duplicates and sort descending
        except ValueError:
            print("Invalid input. No notes moved.")
            input("Press Enter to continue...")
            return

    selected_notes = [notes_list[idx] for idx in indices if 0 <= idx < len(notes_list)]

    # Prepare folder options
    folders = current_section.get("submenus", {})
    folder_keys = list(folders.keys())

    print("Where would you like to move the selected notes?")
    if parent_section:
        print("0. Move to Parent Folder")
    for i, folder in enumerate(folder_keys, 1):
        print(f"{i}. {folder.replace('_', ' ').title()}")

    # Prompt user for target folder
    target_choice = input("Enter your choice (or press Enter to cancel): ").strip()
    if not target_choice:
        print("No target folder selected. Returning to menu.")
        input("Press Enter to continue...")
        return

    if target_choice == "0" and parent_section:
        # Move notes to parent folder
        parent_section.setdefault("notes", []).extend(selected_notes)
        for idx in indices:
            if 0 <= idx < len(notes_list):
                notes_list.pop(idx)
        print("Selected notes moved to the parent folder successfully.")
    elif target_choice.isdigit():
        folder_index = int(target_choice) - 1
        if 0 <= folder_index < len(folder_keys):
            # Move notes to a selected subfolder
            target_folder_key = folder_keys[folder_index]
            target_folder = folders[target_folder_key]
            target_folder.setdefault("notes", []).extend(selected_notes)
            for idx in indices:
                if 0 <= idx < len(notes_list):
                    notes_list.pop(idx)
            print(f"Selected notes moved to '{target_folder_key.replace('_', ' ').title()}' successfully.")
        else:
            print("Invalid folder number. Returning to menu.")
    else:
        print("Invalid input. Returning to menu.")

    save_notes(notes)
    input("Press Enter to continue...")


def add_folder(folders, notes):
    """Add a new folder."""
    folder_name = input("Enter the name of the new folder (or press Enter to cancel): ").strip().replace(' ', '_').lower()
    if not folder_name:
        print("No folder added. Returning to the menu.")
        input("Press Enter to continue...")
        return
    if folder_name in folders:
        print("Folder already exists. Returning to the menu.")
    else:
        folders[folder_name] = {"notes": [], "submenus": {}}
        save_notes(notes)
        print(f"Folder '{folder_name.replace('_', ' ').title()}' added successfully!")
    input("Press Enter to continue...")

def edit_folder(folders, notes):
    """Edit the name of an existing folder."""
    if not folders:
        print("No folders to edit. Returning to the menu.")
        input("Press Enter to continue...")
        return

    # Display the list of folders
    folder_keys = list(folders.keys())
    print("Available Folders:")
    for i, folder in enumerate(folder_keys, 1):
        print(f"{i}. {folder.replace('_', ' ').title()}")

    # Prompt user to select a folder to edit
    choice = input("Enter the folder number to edit (or press Enter to cancel): ").strip()

    if not choice:
        print("No folder selected. Returning to the menu.")
        input("Press Enter to continue...")
        return

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(folder_keys):
            current_name = folder_keys[idx]
            print(f"Current folder name: {current_name.replace('_', ' ').title()}")
            new_name = input("Enter the new name (or press Enter to cancel): ").strip().replace(' ', '_').lower()
            if not new_name:
                print("No changes made. Returning to the menu.")
            elif new_name in folders and new_name != current_name:
                print("A folder with this name already exists. No changes made.")
            else:
                folders[new_name] = folders.pop(current_name)
                save_notes(notes)
                print("Folder name updated successfully!")
        else:
            print("Invalid folder number. Returning to the menu.")
    else:
        print("Invalid input. Returning to the menu.")
    input("Press Enter to continue...")


def delete_folders(folders, notes):
    """Delete multiple folders from the current section."""
    if not folders:
        print("No folders to delete. Returning to the menu.")
        input("Press Enter to continue...")
        return

    # List available folders
    folder_keys = list(folders.keys())
    print("Available Folders:")
    for i, folder in enumerate(folder_keys, 1):
        print(f"{i}. {folder.replace('_', ' ').title()}")

    # Prompt user for folder numbers to delete
    selected = input("Enter the folder numbers to delete (comma-separated, or press Enter to cancel): ").strip()

    if not selected:
        print("No folders selected. Returning to the menu.")
        input("Press Enter to continue...")
        return

    try:
        indices = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]
        indices = sorted(set(indices), reverse=True)  # Remove duplicates and sort descending

        for idx in indices:
            if 0 <= idx < len(folder_keys):
                folder_key = folder_keys[idx]
                confirm = input(f"Are you sure you want to delete '{folder_key.replace('_', ' ').title()}'? (y/n): ").lower()
                if confirm == 'y':
                    del folders[folder_key]
                    print(f"Folder '{folder_key.replace('_', ' ').title()}' deleted.")
                else:
                    print(f"Deletion of folder '{folder_key.replace('_', ' ').title()}' canceled.")
            else:
                print(f"Invalid folder number: {idx + 1}. Skipping.")

        save_notes(notes)
        print("Folder deletion process completed.")
    except ValueError:
        print("Invalid input. No folders deleted.")
    input("Press Enter to continue...")


def move_folders_to_folder(current_folders, parent_section, notes):
    """
    Move one or more folders to another folder or to the parent folder.
    """
    if not current_folders:
        print("No folders available to move.")
        input("Press Enter to continue...")
        return

    # List available folders
    folder_keys = list(current_folders.keys())
    print("Available Folders:")
    for i, folder in enumerate(folder_keys, 1):
        print(f"{i}. {folder.replace('_', ' ').title()}")

    # Prompt user for folder numbers to move
    selected = input("Enter the folder numbers to move (comma-separated, or press Enter to cancel): ").strip()
    if not selected:
        print("No folders selected. Returning to menu.")
        input("Press Enter to continue...")
        return

    try:
        indices = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]
        indices = sorted(set(indices), reverse=True)  # Remove duplicates and sort descending

        selected_folders = [folder_keys[idx] for idx in indices if 0 <= idx < len(folder_keys)]

        if not selected_folders:
            print("Invalid folder selection. Returning to menu.")
            input("Press Enter to continue...")
            return

        # Show options: Move to parent folder or another folder
        print("Where would you like to move the selected folders?")
        if parent_section is not None:
            print("0. Move to parent folder")
        for i, folder in enumerate(folder_keys, 1):
            if folder not in selected_folders:
                print(f"{i}. {folder.replace('_', ' ').title()}")

        # Prompt user for the target
        target_choice = input("Enter the number for the target folder (or press Enter to cancel): ").strip()
        if not target_choice.isdigit():
            print("No valid target selected. Returning to menu.")
            input("Press Enter to continue...")
            return

        target_idx = int(target_choice)
        if target_idx == 0 and parent_section is not None:
            # Move to parent folder
            for folder_key in selected_folders:
                parent_section.setdefault("submenus", {})[folder_key] = current_folders.pop(folder_key)
            save_notes(notes)
            print("Selected folders moved to the parent folder successfully.")
        elif 1 <= target_idx <= len(folder_keys) and folder_keys[target_idx - 1] not in selected_folders:
            # Move to another folder
            target_folder_key = folder_keys[target_idx - 1]
            target_folder = current_folders[target_folder_key]
            for folder_key in selected_folders:
                target_folder.setdefault("submenus", {})[folder_key] = current_folders.pop(folder_key)
            save_notes(notes)
            print(f"Selected folders moved to '{target_folder_key.replace('_', ' ').title()}' successfully.")
        else:
            print("Invalid target selection. Returning to menu.")
    except ValueError:
        print("Invalid input. No folders moved.")
    input("Press Enter to continue...")




def arrange_folders_order(folders, notes):
    """Arrange the order of folders."""
    if not folders:
        print("No folders available to arrange.")
        input("Press Enter to continue...")
        return

    # List current folder order
    folder_keys = list(folders.keys())
    print("Current Folder Order:")
    for i, folder in enumerate(folder_keys, 1):
        print(f"{i}. {folder.replace('_', ' ').title()}")

    # Prompt user for new order
    print("Enter the new order of folder numbers, separated by commas (e.g., '3,1,2'), or press Enter to cancel:")
    new_order_input = input("New Order: ").strip()

    if not new_order_input:
        print("No changes made. Returning to menu.")
        input("Press Enter to continue...")
        return

    try:
        # Parse the new order
        new_order_indices = [int(x.strip()) - 1 for x in new_order_input.split(",") if x.strip().isdigit()]

        # Validate the new order
        if sorted(new_order_indices) != list(range(len(folder_keys))):
            raise ValueError("Invalid order. Please ensure all folder numbers are included exactly once.")

        # Reorder folders
        reordered_folders = {folder_keys[idx]: folders[folder_keys[idx]] for idx in new_order_indices}

        # Update the folder structure
        folders.clear()
        folders.update(reordered_folders)

        save_notes(notes)
        print("Folders reordered successfully.")
    except ValueError as e:
        print(f"Error: {e}. No changes made.")
    input("Press Enter to continue...")


