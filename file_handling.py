import os
import sys
import shutil

global scanlist
scanlist = []

# Get the list of files in the current directory


# Print the names of the files
def listscans(path="."):
    files = os.listdir(path)
    print("Approved files in the current directory:")
    scanlist = [
        file
        for file in files
        if file.startswith("scan") and file.endswith((".pdf", ".jpeg", ".png"))
    ]
    for file in scanlist:
        print(file)
    return scanlist


def rename_scans(oldname, newname):
    print(f"Renaming '{oldname}' to '{newname}'...")
    os.rename(oldname, newname)
    print(f"Renamed '{oldname}' to '{newname}'")


def folderize(path="."):
    files = os.listdir(path)
    scan_files = [file for file in files if file.startswith("OD")]
    file_dates = [file.split("_")[-1] for file in scan_files]
    months_and_days = [file_date.split("-")[:2] for file_date in file_dates]

    i = 0
    for date in months_and_days:
        date = f"{date[0]}-{date[1]}"
        months_and_days[i] = date
        i += 1

    months_and_days = set(months_and_days)

    for month_and_day in months_and_days:
        if os.path.exists(month_and_day):
            for file in scan_files:
                if month_and_day in file:
                    shutil.move(file, os.path.join(month_and_day, file))
                    print(f"{file} moved to directory {month_and_day}.")
        else:
            os.makedirs(month_and_day)
            for file in scan_files:
                if month_and_day in file:
                    shutil.move(file, os.path.join(month_and_day, file))
                    print(f"{file} moved to directory {month_and_day}.")

    # print(file)
    # print(month_and_day)


def folderize_no_reference(file):
    if os.path.exists("Reference_not_found"):
        shutil.move(file, os.path.join("Reference_not_found", file))
        print(f"{file} moved to Reference_not_found.")
    else:
        os.makedirs("Reference_not_found")
        shutil.move(file, os.path.join("Reference_not_found", file))
        print(f"{file} moved to directory Reference_not_found")


def folderize_no_date(file):
    if os.path.exists("Date_not_found"):
        shutil.move(file, os.path.join("Date_not_found", file))
        print(f"{file} moved to Date_not_found.")
    else:
        os.makedirs("Date_not_found")
        shutil.move(file, os.path.join("Date_not_found", file))
        print(f"{file} moved to directory Date_not_found")


def move_pdfs_to_folder(start_dir, target_folder, *args):
    # Create the target folder if it doesn't exist
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    if "cwd" in args:
        start_dir = os.getcwd()
        target_folder = os.path.join(start_dir, target_folder)

    # Walk through all directories and files
    for dirpath, _, filenames in os.walk(start_dir):
        for filename in filenames:
            # Check if the file is a PDF
            if filename.lower().endswith(".pdf"):
                # Create full file path
                file_path = os.path.join(dirpath, filename)

                # Move/Copy the PDF file to the target folder
                if args and "move" in args:
                    try:
                        shutil.move(file_path, os.path.join(target_folder, filename))
                        print(f"Moved: {file_path} to {target_folder}")
                    except shutil.SameFileError:
                        print(f"Same file: {file_path}")
                else:
                    try:
                        shutil.copy(file_path, os.path.join(target_folder, filename))
                        print(f"Copied: {file_path} to {target_folder}")
                    except shutil.SameFileError:
                        print(f"Same file: {file_path}")


def rename_OD_files(directory):
    print(f"Renaming files in '{directory}'...")
    files = os.listdir(directory)
    for file in files:
        if file.endswith(".pdf") and "_" in file:
            old_name = file.split(".")[0]
            new_name = file.replace(old_name, f"scan{old_name}")
            os.rename(os.path.join(directory, file), os.path.join(directory, new_name))
            print(f"Renamed '{file}' to '{new_name}'")


def menu():
    print("""
        Welcome fellow techspotter! What'u want?: 
        1. Folderize
        2. Move all PDFs in directory
        3. Prepend PDFs with 'scan'
        0. Exit
        """)

    option = int(input("Please enter what'u want: "))

    match option:
        case 1:
            folderize()

        case 2:
            cwd = input("Is it in the CWD? (y/n): ")
            if cwd.lower() == "y":
                target_folder = input("Name of destination folder: ")
                move = input("Move instead of copy? (y/n): ")
                if move.lower() == "y":
                    move_pdfs_to_folder("_", target_folder, "cwd", "move")
                else:
                    move_pdfs_to_folder("_", target_folder, "cwd")
            elif cwd.lower() == "n":
                start_dir = input("Please enter starting directory path: ")
                target_folder = input("Please enter target folder path: ")
                move_pdfs_to_folder(start_dir, target_folder)

        case 3:
            target_folder = input("Where are 'em 'OD' PDFs?: ")
            if target_folder == "cwd":
                target_folder == "."
            rename_OD_files(target_folder)

        case 4:
            print("Exiting")
            sys.exit()


if __name__ == "__main__":
    # listscans()
    # oldname = input("Enter the old file name: ")
    # newname = input("Enter the new file name: ")
    # rename_scans(oldname, newname)

    menu()
