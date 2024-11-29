import pytest

from src.core_logic import move_eggs, all_eggs_blocked, is_end_state, no_eggs_left


def test_move_eggs() -> None:
    # Takes in a GRID, DIRECTION, ROWS, COLS, and MOVES_LEFT -> returns a NEW GRID & SCORE

    # Moving Right
    dir = (0, 1)
    assert move_eggs(dir)

    # Moving Left
    dir = (0, -1)
    assert move_eggs(dir)

    # Moving Forward
    dir = (-1, 0)
    assert move_eggs(dir)

    # Moving Backward
    dir = (1, 0)
    assert move_eggs(dir)


def test_all_eggs_blocked() -> None:
    # Takes in a DICT containing the current PUZZLE, ROWS, COLS; and a DIRECTION -> returns a BOOL

    # Moving Right
    dir = (0, 1)
    assert all_eggs_blocked({"puzzle": [], "rows": 0, "cols": 0}, dir)

    # Moving Left
    dir = (0, -1)
    assert all_eggs_blocked({"puzzle": [], "rows": 0, "cols": 0}, dir)

    # Moving Forward
    dir = (-1, 0)
    assert all_eggs_blocked({"puzzle": [], "rows": 0, "cols": 0}, dir)

    # Moving Backward
    dir = (1, 0)
    assert all_eggs_blocked({"puzzle": [], "rows": 0, "cols": 0}, dir)


def test_is_end_state() -> None:
    # Takes in a DICT containing the GRID and MOVES_LEFT -> returns a BOOL
    assert is_end_state({"puzzle": [], "moves_left": 0})


def test_no_eggs_left() -> None:
    # Takes in a GRID -> returns a BOOL
    assert no_eggs_left([])
