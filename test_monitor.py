import hashlib

import monitor
# from unittest import result

from monitor import calculate_hash, validDateFolder, comparison, countUnchangedFiles

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