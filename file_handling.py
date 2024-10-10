import os
import shutil

global scanlist
scanlist = []

# Get the list of files in the current directory


# Print the names of the files
def listscans(path="."):
    files = os.listdir(path)
    print("Approved files in the current directory:")
    scanlist = [file for file in files if file.startswith("scan") and file.endswith((".pdf", ".jpeg", ".png"))]
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
        i+=1
    
    months_and_days = set(months_and_days)    
        
    # Check if the folder exists, if not, create it then move the file there   
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

    

        
if __name__ == "__main__":
    # listscans()
    # oldname = input("Enter the old file name: ")
    # newname = input("Enter the new file name: ")
    # rename_scans(oldname, newname)
    
    folderize()