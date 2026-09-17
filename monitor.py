import hashlib
from pathlib import Path
import json
import os
import sys
# import time

countModifiedFiles = 0
countUnchangedFiles = 0
countNewFilesDetected = 0
countDeletedFiles = 0
skipped_list_count = 0
filePath = "monitor.json"
def load_json(): #load the existing dictionaries from the monitor json file
    with open(filePath, "r") as file:
        loadedJson = json.load(file)
        return loadedJson
#saves the returned dictionary value into new_hashes

def update_json(new_hashes): #dump the value into the monitor.json file
    with open(filePath, "w") as file:
        json.dump(new_hashes, file)

def printSummary():
    print("======================")
    print(f"Modified files: {countModifiedFiles}")
    print(f"Unchanged files: {countUnchangedFiles}")
    print(f"New files: {countNewFilesDetected}")
    print(f"Deleted files: {countDeletedFiles}")
    print(f"Skipped files: {skipped_list_count}")
    print("======================")

userEnterFolderPath = input("Enter the folder path: ")
userChooseSkipExt = input("Do you wish to exclude any file from scanning?:(Y/N) ").lower()
new_hashes = {}
skipped_list = []
while (userEnterFolderPath == ""): #Checks if the path is empty or not, if yes then again asks for the folder path
    print("Path cannot be empty")
    userEnterFolderPath = input("Enter the folder path: ")


def folderScan(userEnterFolderPath, userChooseSkipExt):
    new_hashes = {}
    skipped_list = []
    contentsOfFolder = Path(userEnterFolderPath)
    validateTheInput = ""
    if userChooseSkipExt == 'y':
        print("Tip: Skipping the large files like movies or huge docs can save the scan time")
        validateTheInput = input("Enter the extension you want to exclude:(ex: .pdf, .mkv): ").lower()
        if "." not in validateTheInput:
            print("ERROR! Not a valid file extension")
            sys.exit()
    elif userChooseSkipExt == 'n':
        pass
    else:
        print("Not a valid input\nTry again!")
        sys.exit()
    if not contentsOfFolder.exists(): #Checks for the path user enters and checks it if it exists or not
        return None
    
    if contentsOfFolder.is_file(): #Checks if the path entered is a file
        print(f"'{userEnterFolderPath}' is not a folder")
        return {} #return to stop the program scanning further, also folderScan() requires dictionary thats why I used {}
    for item in contentsOfFolder.rglob("*"): #This .rglob("*") -> will search for the files and folders in the directories and sub-dir recusively in the given path object
        relative_path = item.relative_to(contentsOfFolder) #give me the relative path of the ITEMS which are starting from the monitored root (contentsOfFolder)
        relativePathStr = str(relative_path)

        if item.is_file() and (item.suffix.lower() == validateTheInput or item.suffix.lower() == validateTheInput or item.suffix.lower() == validateTheInput or item.suffix.lower() == validateTheInput or item.suffix.lower() == validateTheInput):
            skipped_list.append(relativePathStr)
            global skipped_list_count
            skipped_list_count+=1
        if item.is_file() and (item.suffix.lower() != validateTheInput and item.suffix.lower() != validateTheInput and item.suffix.lower() != validateTheInput and item.suffix.lower() != validateTheInput and item.suffix.lower() != validateTheInput):
            # start = time.time() #To check how much time does a file takes to scanned
            with open(item, "rb") as file:
                digest = hashlib.file_digest(file, "sha256")
                finalHashResult = digest.hexdigest()
                new_hashes[relativePathStr] = finalHashResult
            # end = time.time()
            # print(f"{relativePathStr} took: {end - start:.2f} Seconds")
    if len(new_hashes) == 0 and len(skipped_list) == 0: #Checks if the folder exists but it has no files
        print(f"'{userEnterFolderPath}' contains no Files")
        sys.exit()
    if len(new_hashes) == 0 and len(skipped_list) != 0:
       for file in skipped_list:
           print(f"'{file}'")
       print(f"Your '{userEnterFolderPath}' contains only excluded file(s)")
       sys.exit()
    return new_hashes, skipped_list #Always save the return value in the variable. One line can return mulitple return variables
         
result = folderScan(userEnterFolderPath, userChooseSkipExt) #Called multiple returns that's why we have to use multiple var to save it
if result is not None:
    new_hashes, skipped_list = result #We unpack only when the result is not none. Tuple unpacking
elif result is None:
    print("ERROR! Path not found")
    sys.exit()

def comparison(old_hashes, new_hashes, skipped_list): #requires parameters because the func doesn't know what we are iterating over
    for key in new_hashes:
        if key in old_hashes:
            if new_hashes[key] != old_hashes[key]:
                print(f"'{key}' was modified")
                global countModifiedFiles #to modify the variable inside the function, python will not think it as a new variable
                countModifiedFiles+=1
            else:
                global countUnchangedFiles
                countUnchangedFiles+=1
            print(key)
        if key not in old_hashes:
            print(f"New file detected: '{key}'")
            global countNewFilesDetected
            countNewFilesDetected+=1

    #Checking if the file is not in the new scanned result, if not then printing it's name
    for key in old_hashes:
        if key not in new_hashes and key in skipped_list:
            print(f"Skipped file '{key}'")
            
        if key not in new_hashes and key not in skipped_list:
            missingFile = key
            print(f"File deleted: {missingFile}")
            global countDeletedFiles
            countDeletedFiles+=1

try:
    # new_hashes, skipped_list = folderScan(userEnterFolderPath)
    if os.path.exists(filePath):
        old_hashes = load_json() 
        #Mistake: Don't call the scanning (Expensive) function again, causes the performance issue.
        comparison(old_hashes, new_hashes, skipped_list)
        printSummary()
        update_json(new_hashes)
        #Giving the access to see the files which were skipped.
        userAccessSkippedFiles = input("Do you wish to see the skipped files?(Y/N): ").lower()
        if userAccessSkippedFiles == "y" and len(skipped_list) != 0:
            for files in skipped_list:
                print(f"'{files}'")
        if userAccessSkippedFiles == 'y' and len(skipped_list) == 0:
            print("No files were skipped")
        elif userAccessSkippedFiles == 'n':
            print("Thankyou")
            sys.exit()
    
    else:
        #Mistake: Don't call the scanning (Expensive) function again, causes the performance issue.
        update_json(new_hashes)
        print("No baseline found\nInitial baseline created successfully\nRun the program again to detect the changes")

except FileNotFoundError:   
    print("Folder not found")
# except TypeError:
#     print("Error! Path not found")
except json.JSONDecodeError:
    print("Json file is empty")

except NotADirectoryError:
    print("Not a folder")

#Note: Video files such as .mpv, .mp4 and .avi etc are currently excluded to reduce the scanning time.
#They are intentionally skipped, not treated as deleted.
#A future version may allow users to configure which file types are monitored or view skipped files individually.

