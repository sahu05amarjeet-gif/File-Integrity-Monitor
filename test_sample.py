import hashlib
from unittest import result

from monitor import calculate_hash, validDateFolder

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


