import pytest

from src.level_manager import get_level_data, can_restart


def test_get_level_data() -> None:
    # Takes in a FILENAME (str)

    # For Puzzle
    assert get_level_data()["puzzle"]

    # For Moves Left
    assert get_level_data()["moves_left"]

    # For Rows and Cols
    assert get_level_data()["rows"], get_level_data()["cols"]
