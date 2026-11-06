import hashlib

import monitor
# from unittest import result

from monitor import calculate_hash, validDateFolder, comparison, countUnchangedFiles, folderScan

def test_calculate_hash(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello world")
    byted = file_path.read_bytes()
    expectedShaValue = hashlib.sha256(byted)
    expectedHash = expectedShaValue.hexdigest()
    actualHash = calculate_hash(file_path)
    assert expectedHash == actualHash

def test_validate_folder(tmp_path):
    file_path = tmp_path / "testValidateFolder.txt"
    folder = tmp_path / "my_test_folder"
    non_existing_file = tmp_path / "non_exisiting_file.txt"
    folder.mkdir()
    result1 = validDateFolder(folder)

    file_path.write_text("Hello world")
    result2 = validDateFolder(file_path)

    result3 = validDateFolder(non_existing_file)
    assert result1 == True
    assert result2 == False
    assert result3 == False

def test_comparison_unchanged(tmp_path, monkeypatch):
    file_path = tmp_path / "test_comparison.txt"
#     new_hashes, skipped_list, savedFileWithHashes
#     Unchanged
    current_scan = {file_path : "abcdef1234"}
    previous_scan = {file_path: "abcdef1234"}
    skipped_scan = []
    monkeypatch.setattr(monitor, "countUnchangedFiles", 0)
    comparison(current_scan, skipped_scan, previous_scan)
    assert monitor.countUnchangedFiles == 1

def test_comparison_modified(tmp_path, monkeypatch):
    file_path = tmp_path / "test_modified_comparison.txt"
    # Modified files
    currentScan = {file_path: "abcccdd3344"}
    previousScan = {file_path: "abbccdde3345"}
    skippedScan = []
    monkeypatch.setattr(monitor, "countModifiedFiles", 0)
    comparison(currentScan, skippedScan, previousScan)
    assert monitor.countModifiedFiles == 1

def test_comparison_new_file_detected(tmp_path, monkeypatch):
    old_file = tmp_path / "old_file.txt"
    new_file = tmp_path / "new_file.txt"
    currentScan = {new_file : "abc345"}
    previousScan = {old_file : "abc345"}
    skippedScan = []
    monkeypatch.setattr(monitor, "countNewFilesDetected", 0)
    comparison(currentScan, skippedScan, previousScan)
    assert monitor.countNewFilesDetected == 1

def test_comparison_deleted_files(tmp_path, monkeypatch):
    old_file = tmp_path / "old_file.txt"
    new_file = tmp_path / "new_file.txt"
    currentScan = {new_file: "abc345"}
    previousScan = {old_file: "abc345"}
    skippedScan = []
    monkeypatch.setattr(monitor, "countDeletedFiles", 0)
    comparison(currentScan, skippedScan, previousScan)
    assert monitor.countDeletedFiles == 1

def test_folder_scan_new_hashes(tmp_path, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    first_folder = tmp_path / "first_folder"
    first_folder.mkdir()
    first_file = first_folder / "first_text.txt"
    second_file = first_folder / "second_text.txt"
    first_file.write_text("Hello World!")
    second_file.write_text("Hello")
    folder_scan = folderScan(first_folder)
    hashes, skipped = folderScan(first_folder)
    first_file_hash = calculate_hash(first_file)
    second_file_hash = calculate_hash(second_file)
    total = {"first_text.txt" : first_file_hash, #Relative file path name
             "second_text.txt" : second_file_hash}
    assert hashes == total

def test_folder_exclusion(tmp_path, monkeypatch):
    inputs = ["y", ".jpg", "n"]
    input_iterator = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda  _: next(input_iterator))
    folder = tmp_path / "check_exclusion"
    folder.mkdir()
    notes = folder / "notes.txt"
    notes.write_text("This is our notes of Java Programming")
    photos = folder / "photo.jpg"
    photos.write_text("doraemon-and-nobita")
    pdfs = folder / "document.pdf"
    pdfs.write_text("school_docs")
    hashes, skipped_list = folderScan(folder)
    assert "photo.jpg" in skipped_list
    assert "notes.txt" in hashes
    assert "document.pdf" in hashes
    assert "photo.jpg" not in hashes

def test_folder_multiple_exclusion(tmp_path, monkeypatch):
    inputs = ["y", ".mkv", "y", ".pdf"]
    inputs_iter = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_iter))
    folder = tmp_path / "test_multiple_exclusion"
    folder.mkdir()

    document = folder / "document.pdf"
    document.write_text("OOPs in java vs Python")
    photo = folder / "photo.jpg"
    photo.write_text("happy_pics")
    text = folder / "text.txt"
    text.write_text("encryption")
    movie = folder / "movie.mkv"
    movie.write_text("lost-1080p-fhd")
    hashes, skipped_file = folderScan(folder)

    assert "movie.mkv" in skipped_file
    assert "document.pdf" in skipped_file
    assert "photo.jpg" in hashes
    assert "text.txt" in hashes
    assert "movie.mkv" not in hashes
    assert "document.pdf" not in hashes


