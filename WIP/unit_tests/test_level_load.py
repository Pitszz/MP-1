import pytest
from game import LoadLevel


# The functions with no return or yielded values are NOT unit tested.

# LEVEL TEST


def test_load_level():
    # Takes a FILENAME -> returns a DICT
    
    # TEST CASE 1
    file_name = "level1.in"
    level1 = LoadLevel(['mock', file_name])
    level_data = level1.level_data

    assert level_data.puzzle == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]
    assert level_data.max_moves == 5
    assert level_data.rows, level_data.cols == (4, 8)

    # TEST CASE 2
    file_name_2 = "level9.in"
    level2 = LoadLevel(['mock', file_name_2])
    level_data_2 = level2.level_data

    assert level_data_2.puzzle == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🥚", "🥚", "🥚", "🧱", "🍳", "🟩", "🟩", "🧱"],
    ["🧱", "🟩", "🧱", "🥚", "🧱", "🟩", "🧱", "🧱", "🧱"],
    ["🧱", "🥚", "🥚", "🟩", "🪹", "🪹", "🪹", "🟩", "🧱"],
    ["🧱", "🟩", "🧱", "🧱", "🧱", "🟩", "🟩", "🪹", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🟩", "🟩", "🟩", "🪹", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱", "🪹", "🍳", "🟩", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]
    assert level_data_2.max_moves == 60
    assert level_data_2.rows, level_data_2.cols == (9, 9)


    # TEST CASE 3
    file_name_3 = "level4.in"
    level3 = LoadLevel(['mock', file_name_3])
    level_data_3 = level3.level_data

    assert level_data_3.puzzle == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🪹", "🟩", "🟩", "🍳", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🟩", "🥚", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🪹", "🟩", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🍳", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🪹", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🟩", "🧱"],
    ["🧱", "🥚", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🪹", "🟩", "🟩", "🟩", "🟩", "🧱"],
    ["🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🥚", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🍳", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🧱"],
    ["🧱", "🧱", "🍳", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🧱"],
    ["🧱", "🥚", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🪹", "🟩", "🟩", "🍳", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🟩", "🟩", "🧱", "🧱", "🥚", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]
    assert level_data_3.max_moves == 15
    assert level_data_3.rows, level_data_3.cols == (19, 19)


    # TEST CASE 4
    file_name_4 = "levelcl.in"
    level4 = LoadLevel(['mock', file_name_4])
    level_data_4 = level4.level_data

    assert level_data_4.puzzle == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🍳", "🥚", "🥚", "🥚", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱", "🟩", "🧱"],
    [" ", "🧱", "🧱", "🧱", " ", " ", " ", " ", "🟩", "🧱", "🟩", " "],
    ["🧱", "🪹", "🟩", "🟩", "🥚", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
    [" ", "🧱", "🧱", "🟩", " ", " ", " ", " ", "🪹", "🟩", "🟩", " "], 
    ["🧱", "🧱", "🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🧱"],
    ["🧱", "🪹", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🪹", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ]
    assert level_data_4.max_moves == 15
    assert level_data_4.rows, level_data_3.cols == (9, 12)

    # Level not in levels Folder (System Exits)
    file_name_x = "levelmissing.in"
    file_name_y = "levelhaha.in"
    file_name_z = "leveltest.in"

    with pytest.raises(SystemExit):
        # automatically goes to load_level() after initialization
        assert LoadLevel(['mock', file_name_x])
        assert LoadLevel(['mock', file_name_y])
        assert LoadLevel(['mock', file_name_z])