# File Integrity Monitor

A Python-based file integrity monitoring tool that uses SHA-256 hashing to detect changes in files through recursive folder scanning.

This project is currently under development and is being built incrementally to improve my understanding of file systems, file handling, hashing, recursion, JSON storage, and cybersecurity concepts.

## Features

* Calculates SHA-256 hashes for files.
* Stores file paths and hashes in a JSON baseline.
* Detects modified files.
* Detects unchanged files.
* Detects newly added files.
* Detects deleted files.
* Scans files inside subfolders recursively.
* Displays a summary of detected changes.
* Includes basic input validation.

## How It Works

1. The user enters the folder path to monitor.
2. The program recursively scans the folder and its subfolders.
3. A SHA-256 hash is calculated for every discovered file.
4. File paths and hashes are stored in a dictionary.
5. The dictionary is saved as a JSON baseline.
6. On later runs, the new scan is compared with the previous baseline.
7. The program reports modified, unchanged, new, and deleted files.

## Technologies Used

* **Python**
* `hashlib` — SHA-256 file hashing
* `pathlib` — file and directory path handling
* `json` — storing and loading hash data
* `os` — path and file-system checks

## Project Structure

```text
File-Integrity-Monitor/
│
├── monitor.py
├── README.md
├── .gitignore
└── monitor.json
```

> The project structure may change as development continues.

## How to Run

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

### 2. Enter the project directory

```bash
cd File-Integrity-Monitor
```

### 3. Run the program

```bash
python monitor.py
```

### 4. Enter the folder path

When prompted, enter the path of the folder you want to monitor.

Example:

```text
Practice/test_folder
```

## Example Output

```text
======================
Modified files: 1
Unchanged files: 3
New files: 1
Deleted files: 0
======================
```

## Current Limitations

* Monitoring currently happens through repeated manual scans.
* Real-time monitoring has not yet been implemented.
* Error handling and input validation are still being improved.
* The project does not yet have a graphical user interface.

## Future Improvements

* Add real-time monitoring using the `watchdog` library.
* Improve invalid-path and empty-folder handling.
* Add timestamps to change reports.
* Add logging for detected changes.
* Create a PyQt5 graphical interface.
* Improve configuration and portability.
* Add automated tests.

## Development History

The project was initially developed inside my Python practice repository, where I made commits while learning and implementing its features.

After developing the core functionality, I moved the project into this independent repository to maintain a cleaner structure and document its future development.

## Learning Outcomes

This project is helping me practice:

* File and directory handling
* Absolute and relative paths
* Recursive directory traversal
* Reading and writing files
* SHA-256 hashing
* Dictionary comparison
* JSON persistence
* Debugging and input validation

## Status

**Under development**

This repository documents my progress as I continue learning Python and exploring cybersecurity-related concepts.

## License

This project is intended for educational and learning purposes.
