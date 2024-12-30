def search_notes(notes):
    """Search for a keyword in all notes."""
    keyword = input("Enter a keyword to search (or press Enter to cancel): ").strip()

    if not keyword:
        print("No keyword entered. Returning to the main menu.")
        input("Press Enter to continue...")
        return

    print(f"Searching for '{keyword}'...\n")

    # Recursive function to search notes within folders
    def search_section(section, path=""):
        found = False
        for note in section.get("notes", []):
            if keyword.lower() in note.lower():
                print(f"Found in {path or '[Main Folder]'}: {note}")
                found = True
        for folder, content in section.get("submenus", {}).items():
            if search_section(content, path + " > " + folder.replace("_", " ").title()):
                found = True
        return found

    # Start the search
    if not search_section(notes["r_cheatsheet"]):
        print("No matches found.")

    input("\nPress Enter to return to the main menu.")
