import pytest

from src.level_manager import get_level_data, can_restart


def test_get_level_data() -> None:
    # Takes in a FILENAME (str) -> returns a DICT containing all the relevant info

    # For Puzzle or Grid
    assert get_level_data()["initial_state"]

    # For Max Moves
    assert get_level_data()["max_moves"]

    # For Rows and Cols
    assert get_level_data()["rows"], get_level_data()["cols"]
