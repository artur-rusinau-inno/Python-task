import pytest

from src.managers import SaveManager


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


def test_save_manager(tmp_path, rooms_data, students_data):
    rooms_path = SaveManager(rooms_data).save(tmp_path)
    students_path = SaveManager(students_data).save(tmp_path)

    assert rooms_path.is_file()
    assert students_path.is_file()


def test_unknown_format(tmp_path, rooms_data):
    with pytest.raises(ValueError):
        SaveManager(rooms_data).save(tmp_path, "mp3")
