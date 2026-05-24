import pytest

from src.app.file_manager import FileManager


@pytest.fixture
def rooms_data():
    data = [{"id": i, "name": f"test_room_{i}"} for i in range(1, 6)]
    return data


@pytest.fixture
def students_data():
    data = [
        {
            "birthday": f"2000-01-0{i}T00:00:00.000000",
            "id": i,
            "name": f"test_student_{i}",
            "room": f"test_room_{i}",
            "sex": "M" if i % 2 else "F",
        }
        for i in range(1, 6)
    ]
    return data


def test_file_manager_save(tmp_path, rooms_data, students_data):
    rooms_file = FileManager.save(rooms_data, tmp_path, "json")
    students_file = FileManager.save(students_data, tmp_path, "xml")

    print(rooms_file.read_text())

    assert rooms_file.exists()
    assert students_file.exists()


def test_unknown_format(tmp_path, rooms_data):
    with pytest.raises(ValueError):
        FileManager.save(rooms_data, tmp_path, "XXX")
