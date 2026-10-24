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
    baseline = {
        "folder_path": userEnterFolderPath,
        "files": new_hashes
    }
    with open(filePath, "w") as file:
        json.dump(baseline, file, default = str)

def printSummary():
    print("======================")
    print(f"Modified files: {countModifiedFiles}")
    print(f"Unchanged files: {countUnchangedFiles}")
    print(f"New files: {countNewFilesDetected}")
    print(f"Deleted files: {countDeletedFiles}")
    print(f"Skipped files: {skipped_list_count}")
    print("======================")
print("================================================")
userEnterFolderPath = Path(input("Enter the folder path: ")).resolve()
print("================================================")

new_hashes = {}
folderPath = {}
skipped_list = []
while (userEnterFolderPath == ""): #Checks if the path is empty or not, if yes then again asks for the folder path
    print("Path cannot be empty")
    print("================================================")
    userEnterFolderPath = input("Enter the folder path: ")
    print("================================================")


def folderScan(userEnterFolderPath):
    new_hashes = {}
    skipped_list = []
    validExtensions = (
    ".jpg", ".jpeg", ".pdf", ".png", ".mkv", ".mov", ".mp4", 
    ".wav", ".avi", ".mp3", ".gif", ".svg", ".webp", ".doc",
    ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", 
    ".rtf", ".txt", ".csv", ".zip", ".rar", ".7z", ".tar", 
    ".gz", ".tar.gz", ".tgz"
)
    contentsOfFolder = Path(userEnterFolderPath)
    validateTheInput = ""
    validateDoubleInput =""
    if not contentsOfFolder.exists(): #Checks for the path user enters and checks it if it exists or not
        return None
    
    if contentsOfFolder.is_file(): #Checks if the path entered is a file
        print(f"'{userEnterFolderPath}' is not a file")
        sys.exit() #to avoid any program to move further,as it will cause unpacking error
    print("=======================================================")
    userChooseSkipExt = input("Do you wish to exclude any file from scanning?(Y/N): ").lower()
    print("=======================================================")
    if userChooseSkipExt == 'n':
            print("NOTE: SCANNING ENTIRELY WILL TAKE SOME TIME AS IT WILL SCAN THROUGH THE ENTIRE HUGE FILES TOO IN A FOLDER")
            pass
    elif userChooseSkipExt == 'y':
        print("")
        print("******************************************************************************")
        print("Tip: Skipping the large files like movies or huge docs can save the scan time")
        print("******************************************************************************")
        print("")
        print("==============================================================")
        validateTheInput = input("Enter the extension you want to exclude:(ex: .pdf, .mkv): ").lower()
        print("=============================================================")
        # Check if the entered extension is correct and if it doesnt exists in the entered path
        while not validateTheInput.endswith(validExtensions):
            print("ERROR! Not a valid file extension")
            print("==============================================================================")
            validateTheInput = input("Enter the extension you want to exclude:(ex: .pdf, .mkv): ").lower()
            print("==============================================================================")

            
        print("==============================================================")
        doubleInput = input("Do you want to skip more files?:(Y/N): ").lower()
        print("==============================================================")
        if doubleInput == 'y':
            print("==============================================================================")
            validateDoubleInput = input("Enter the extension you want to exclude:(ex: .pdf, .mkv): ").lower()
            print("==============================================================================")

            while not validateDoubleInput.endswith(validExtensions):
                print("ERROR! Not a valid file extension")
                print("==============================================================================")
                validateDoubleInput = input("Enter the extension you want to exclude:(ex: .pdf, .mkv): ").lower()
                print("==============================================================================")
        elif doubleInput == 'n':
            pass
        else:
            print("Not a valid input\nTry again!")
            sys.exit()
    else:
        print("Not a valid input\nTry again!")
        sys.exit()
                
          
    
    for item in contentsOfFolder.rglob("*"): #This .rglob("*") -> will search for the files and folders in the directories and sub-dir recusively in the given path object
        relative_path = item.relative_to(contentsOfFolder) #give me the relative path of the ITEMS which are starting from the monitored root (contentsOfFolder)
        relativePathStr = str(relative_path)

        if item.is_file() and (item.suffix.lower() == validateTheInput or item.suffix.lower() == validateDoubleInput):
            skipped_list.append(relativePathStr)
            global skipped_list_count
            skipped_list_count+=1
        if item.is_file() and (item.suffix.lower() != validateTheInput and item.suffix.lower() != validateDoubleInput):
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


def comparison(new_hashes, skipped_list, savedFilesWithHash): #requires parameters because the func doesn't know what we are iterating over
    for key in new_hashes:
        if key in savedFilesWithHash:
            if new_hashes[key] != savedFilesWithHash[key]:
                print(f"'{key}' was modified")
                global countModifiedFiles #to modify the variable inside the function, python will not think it as a new variable
                countModifiedFiles+=1
            else:
                global countUnchangedFiles
                countUnchangedFiles+=1
            print(key)
        if key not in savedFilesWithHash:
            print(f"New file detected: '{key}'")
            global countNewFilesDetected
            countNewFilesDetected+=1

    #Checking if the file is not in the new scanned result, if not then printing it's name
    for key in savedFilesWithHash:
        if key not in new_hashes and key in skipped_list:
            pass
            
        if key not in new_hashes and key not in skipped_list:
            missingFile = key
            print(f"File deleted: {missingFile}")
            global countDeletedFiles
            countDeletedFiles+=1

try:
    if os.path.exists(filePath):
        returnedDic = load_json()

        savedFolderPath = Path(returnedDic["folder_path"]).resolve()
        savedFilesWithHash = returnedDic["files"]

        if savedFolderPath != userEnterFolderPath:
            print("Baseline exists, belongs to different folder")
            sys.exit()

        print("Path check reached")

        result = folderScan(userEnterFolderPath)

        if result is None:
            print("ERROR! Path not found")
            sys.exit()

        new_hashes, skipped_list = result

        comparison(new_hashes, skipped_list, savedFilesWithHash)

        printSummary()

        update_json(new_hashes)

    else:
        result = folderScan(userEnterFolderPath)

        if result is None:
            print("ERROR! Path not found")
            sys.exit()

        new_hashes, skipped_list = result

        update_json(new_hashes)

        print("No baseline found")
        print("Initial baseline created successfully")
        print("Run the program again to detect the changes")

except Exception as e:
    print(f"An error occurred: {e}")
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

