import hashlib
from pathlib import Path
import json
import os
import sys
import time

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

def update_json(): #dump the value into the monitor.json file
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
new_hashes = {}
skipped_list = []
while (userEnterFolderPath == ""): #Checks if the path is empty or not, if yes then again asks for the folder path
    print("Path cannot be empty")
    userEnterFolderPath = input("Enter the folder path: ")


def folderScan(userEnterFolderPath):
    new_hashes = {}
    skipped_list = []
    contentsOfFolder = Path(userEnterFolderPath)
    if not contentsOfFolder.exists(): #Checks for the path user enters and checks it if it exists or not
        return None
    
    if contentsOfFolder.is_file(): #Checks if the path entered is a file
        print(f"'{userEnterFolderPath}' is not a folder")
        return {} #return to stop the program scanning further, also folderScan() requires dictionary thats why I used {}
    for item in contentsOfFolder.rglob("*"): #This .rglob("*") -> will search for the files and folders in the directories and sub-dir recusively in the given path object
        relative_path = item.relative_to(contentsOfFolder) #give me the relative path of the ITEMS which are starting from the monitored root (contentsOfFolder)
        relativePathStr = str(relative_path)

        if item.is_file() and item.suffix.lower() == ".mkv" or item.suffix.lower() == ".mp4" or item.suffix.lower() == ".avi" or item.suffix.lower() == ".mov" or item.suffix.lower() == ".wmv":
            skipped_list.append(relativePathStr)
            global skipped_list_count
            skipped_list_count+=1
        if item.is_file() and item.suffix.lower() != ".mkv" and item.suffix.lower() != ".mp4" and item.suffix.lower() != ".avi" and item.suffix.lower() != ".mov" and item.suffix.lower() != ".wmv":
            # start = time.time() 
            with open(item, "rb") as file:
                digest = hashlib.file_digest(file, "sha256")
                finalHashResult = digest.hexdigest()
                new_hashes[relativePathStr] = finalHashResult
            # end = time.time()
            # print(f"{relativePathStr} took: {end - start:.2f} Seconds")
    if len(new_hashes) == 0: #Checks if the folder exists but it has no files
        print(f"'{userEnterFolderPath}' contains no Files")
        return {}
    return new_hashes #Always save the return value in the variable.

new_hashes = folderScan(userEnterFolderPath)

if new_hashes is None:
    print("ERROR: Folder path not found")
    sys.exit()

def comparison(old_hashes, new_hashes): #requires parameters because the func doesn't know what we are iterating over
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
            print("Skipped file")
            
        if key not in new_hashes and key not in skipped_list:
            missingFile = key
            print(f"File deleted: {missingFile}")
            global countDeletedFiles
            countDeletedFiles+=1

try:
    if os.path.exists(filePath):
        old_hashes = load_json() 
        #Mistake: Don't call the scanning (Expensive) function again, causes the performance issue.
        comparison(old_hashes, new_hashes)
        printSummary()
        update_json()
    else:
        #Mistake: Don't call the scanning (Expensive) function again, causes the performance issue.
        print("No baseline found\nInitial baseline created successfully\nRun the program again to detect the changes")
        update_json()

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

