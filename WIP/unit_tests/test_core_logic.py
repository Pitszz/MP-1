import pytest
from random import randint, choice
import copy
from game import Dir, LevelData, Game, Egg, Display


# The functions with no return or yielded values are NOT unit tested.
# Inner functions are also not unit tested.

# CORE LOGIC TESTS

class GameIt(Game):
    # a subclass created to bypass the initializer
    def __init__(self):
        # bypass __init__ (probably not a good idea)
        # but if it works, it works
        pass


test = GameIt()


mock_level_data = LevelData(
    rows = 0,
    cols = 0,
    max_moves = 10,
    moves_left = 10**4, 
    points = [0],
    previous_moves = [],
    current_move = '',
    puzzle = [],
    )
egg_test = Egg(mock_level_data, Display(mock_level_data))
# basic test object


def test_move_eggs() -> None:
    # Takes in a GRID, DIRECTION, ROWS, COLS, and LEVEL_DATA -> returns
    # a NEW GRID

    # I haven't found a better way to test than to keep using a
    # different copy of mock_level_data_x to create a new instance that
    # is referentially different to prevent side effects

    # TEST CASE 1
    mock_level_data_1 = LevelData(
        rows = 4, 
        cols = 8,
        max_moves = 10,
        moves_left = 5,
        points = [0],
        previous_moves = [],
        current_move = '',
        puzzle = [
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ]
        )

    rows, cols = mock_level_data_1.rows, mock_level_data_1.cols

    # Moving Right
    mock_copy = copy.deepcopy(mock_level_data_1)
    egg_test_1 = Egg(mock_copy, Display(mock_copy))
    puzzle = [row[:] for row in mock_level_data_1.puzzle]
    assert egg_test_1.move_eggs(puzzle, Dir.RIGHT, rows, cols, mock_copy) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Moving Left
    mock_copy = copy.deepcopy(mock_level_data_1)
    egg_test_1 = Egg(mock_copy, Display(mock_copy))
    puzzle = [row[:] for row in mock_level_data_1.puzzle]
    assert egg_test_1.move_eggs(puzzle, Dir.LEFT, rows, cols, mock_copy) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🪹", "🪹", "🟩", "🥚", "🥚", "🟩", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Moving Forward/Up
    mock_copy = copy.deepcopy(mock_level_data_1)
    egg_test_1 = Egg(mock_copy, Display(mock_copy))
    puzzle = [row[:] for row in mock_level_data_1.puzzle]
    assert egg_test_1.move_eggs(puzzle, Dir.FORWARD, rows, cols, mock_copy) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Moving Backward/Down
    mock_copy = copy.deepcopy(mock_level_data_1)
    egg_test_1 = Egg(mock_copy, Display(mock_copy))
    puzzle = [row[:] for row in mock_level_data_1.puzzle]
    assert egg_test_1.move_eggs(puzzle, Dir.BACKWARD, rows, cols, mock_copy) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🟩", "🟩", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🥚", "🍳", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # TEST CASE 2
    mock_level_data_2 = LevelData(
        rows = 5, 
        cols = 5,
        max_moves = 10,
        moves_left = 5,
        points = [0],
        previous_moves = [],
        current_move = '',
        puzzle = [
        ["🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🟩", "🍳", "🟩", "🧱"],
        ["🧱", "🪹", "🥚", "🍳", "🧱"],
        ["🧱", "🪹", "🥚", "🟩", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱"]
        ]
        )
    egg_test_2 = Egg(mock_level_data_2, Display(mock_level_data_2))

    rows_2, cols_2 = mock_level_data_2.rows, mock_level_data_2.cols

    # Moving Right
    mock_copy_2 = copy.deepcopy(mock_level_data_2)
    egg_test_2 = Egg(mock_copy_2, Display(mock_copy_2))
    puzzle_2 = [row[:] for row in mock_level_data_2.puzzle]
    assert egg_test_2.move_eggs(puzzle_2, Dir.RIGHT, rows_2, cols_2, mock_copy_2) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🟩", "🍳", "🧱"],
    ["🧱", "🪹", "🟩", "🥚", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Moving Left
    mock_copy_2 = copy.deepcopy(mock_level_data_2)
    egg_test_2 = Egg(mock_copy_2, Display(mock_copy_2))
    puzzle_2 = [row[:] for row in mock_level_data_2.puzzle]
    assert egg_test_2.move_eggs(puzzle_2, Dir.LEFT, rows_2, cols_2, mock_copy_2) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪺", "🟩", "🍳", "🧱"],
    ["🧱", "🪺", "🟩", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Moving Forward/Up
    mock_copy_2 = copy.deepcopy(mock_level_data_2)
    egg_test_2 = Egg(mock_copy_2, Display(mock_copy_2))
    puzzle_2 = [row[:] for row in mock_level_data_2.puzzle]
    assert egg_test_2.move_eggs(puzzle_2, Dir.FORWARD, rows_2, cols_2, mock_copy_2) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🟩", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Moving Backward/Down
    mock_copy_2 = copy.deepcopy(mock_level_data_2)
    egg_test_2 = Egg(mock_copy_2, Display(mock_copy_2))
    puzzle_2 = [row[:] for row in mock_level_data_2.puzzle]
    assert egg_test_2.move_eggs(puzzle_2, Dir.BACKWARD, rows_2, cols_2, mock_copy_2) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🥚", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]


def test_is_inside() -> None:
    # Takes in I, J, ROWS, and COLS -> returns a BOOL
    rows, cols = 10, 10
    
    assert egg_test.is_inside(0, 0, rows, cols)
    assert egg_test.is_inside(5, 5, rows, cols)
    assert not egg_test.is_inside(10, 10, rows, cols)
    assert not egg_test.is_inside(-1, 0, rows, cols)
    assert not egg_test.is_inside(0, -1, rows, cols)
    assert not egg_test.is_inside(11, 0, rows, cols)
    assert not egg_test.is_inside(7, 10**8, rows, cols)

    # EDGE CASES 

    # ROWS or COLS is 0 (Should evaluate to False since 0 < 0)
    rows, cols = 10, 10
    rows_0, cols_0 = 0, 0

    assert not egg_test.is_inside(0, 6, rows_0, cols)
    assert not egg_test.is_inside(4, 0, rows, cols_0)
    assert not egg_test.is_inside(0, 0, rows_0, cols_0)

    # Really Large ROWS and COLS, Random Cases
    rows, cols = randint(0, 10**6), randint(0, 10**6)
    in_i, in_j = inbound(rows), inbound(cols)
    out_i, out_j = outbound(rows), outbound(cols)

    assert egg_test.is_inside(in_i, in_j, rows, cols)
    assert not egg_test.is_inside(in_i, out_j, rows, cols)
    assert not egg_test.is_inside(out_i, in_j, rows, cols)
    assert not egg_test.is_inside(out_i, out_j, rows, cols)


def test_get_eggs_pos() -> None:
    # Takes in a GRID of LIST[LIST[STR]] -> returns a LIST[TUPLE]
    egg_pos_ld = LevelData(
    rows = 0,
    cols = 0,
    max_moves = 10,
    moves_left = 0, 
    points = [0],
    previous_moves = [],
    current_move = '',
    puzzle = [],
    )

    egg_pos_mock = Egg(egg_pos_ld, Display(egg_pos_ld))
    # clear previous list after since we are still using the same
    # object instance for all tests

    egg_pos_ld.puzzle = [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🥚", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    assert egg_pos_mock.get_eggs_pos(egg_pos_ld.puzzle) == [(2, 2), (3, 2)]
    egg_pos_mock.egg_coordinates.clear()  # clearing previous list

    egg_pos_ld.puzzle = [
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

    assert egg_pos_mock.get_eggs_pos(egg_pos_ld.puzzle) == [(1, 1), (1, 2), (1, 3), (2, 3), (3, 1), (3, 2)]
    egg_pos_mock.egg_coordinates.clear()  # clearing previous list

    egg_pos_ld.puzzle = [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    assert egg_pos_mock.get_eggs_pos(egg_pos_ld.puzzle) == [(1, 5), (1, 6)]
    egg_pos_mock.egg_coordinates.clear()  # clearing previous list

    # No Eggs
    egg_pos_ld.puzzle = [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🟩", "🟩", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    assert egg_pos_mock.get_eggs_pos(egg_pos_ld.puzzle) == []
    egg_pos_mock.egg_coordinates.clear()  # clearing previous list

    # Edge Case: Empty GRID
    egg_pos_ld.puzzle = []
    assert egg_pos_mock.get_eggs_pos(egg_pos_ld.puzzle) == []
    egg_pos_mock.egg_coordinates.clear()  # clearing previous list


    # Edge Case: GRID is a TUPLE[TUPLE[STR]]
    egg_pos_ld.puzzle = (
    ("🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"), 
    ("🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"), 
    ("🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"), 
    ("🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱")
    )

    assert egg_pos_mock.get_eggs_pos(egg_pos_ld.puzzle) == [(1, 5), (1, 6)]
    egg_pos_mock.egg_coordinates.clear()  # clearing previous list
    

def test_all_eggs_blocked() -> None:
    # Takes in a LevelData containing the current PUZZLE, ROWS, COLS; and a DIRECTION -> returns a BOOL
    eggs_blocked_ld = LevelData(
    rows = 0,
    cols = 0,
    max_moves = 10,
    moves_left = 10**4, 
    points = [0],
    previous_moves = [],
    current_move = '',
    puzzle = [],
    )


    # Moving Right
    eggs_blocked_ld.puzzle = [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🥚", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]
    eggs_blocked_ld.rows = 5
    eggs_blocked_ld.cols = 5

    eggs_blocked_mock = Egg(eggs_blocked_ld, Display(eggs_blocked_ld))
    assert not eggs_blocked_mock.all_eggs_blocked(eggs_blocked_ld, Dir.RIGHT)


    # Moving Left  
    eggs_blocked_ld.puzzle = [
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
    eggs_blocked_ld.rows = 9
    eggs_blocked_ld.cols = 9

    eggs_blocked_mock = Egg(eggs_blocked_ld, Display(eggs_blocked_ld)) 
    assert eggs_blocked_mock.all_eggs_blocked(eggs_blocked_ld, Dir.LEFT)


    # Moving Forward
    eggs_blocked_ld.puzzle = [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]
    eggs_blocked_ld.rows = 4
    eggs_blocked_ld.cols = 8

    eggs_blocked_mock = Egg(eggs_blocked_ld, Display(eggs_blocked_ld))
    assert eggs_blocked_mock.all_eggs_blocked(eggs_blocked_ld, Dir.FORWARD)


    # Moving Backward
    eggs_blocked_ld.puzzle = [
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
    eggs_blocked_ld.rows = 19
    eggs_blocked_ld.cols = 19

    eggs_blocked_mock = Egg(eggs_blocked_ld, Display(eggs_blocked_ld)) 
    assert not eggs_blocked_mock.all_eggs_blocked(eggs_blocked_ld, Dir.BACKWARD) 


def test_is_end_state() -> None:
    # Takes in a DICT containing the GRID and MOVES_LEFT -> returns a BOOL
    end_state_mock = LevelData(
    rows = 0,
    cols = 0,
    max_moves = 10,
    moves_left = 0, 
    points = [0],
    previous_moves = [],
    current_move = '',
    puzzle = [],
    )

    # No Egg/s Left, No Moves Left
    end_state_mock.moves_left = 0

    end_state_mock.puzzle = []
    assert test.is_end_state(end_state_mock)

    end_state_mock.puzzle = ["🧱🧱🧱🧱", "🧱🟩🟩🧱", "🧱🟩🟩🧱", "🧱🧱🧱🧱"]
    assert test.is_end_state(end_state_mock)

    end_state_mock.puzzle = ["🧱🧱🧱🧱", "🧱🪺🟩🧱", "🧱🟩🍳🧱", "🧱🧱🧱🧱"]
    assert test.is_end_state(end_state_mock)

    end_state_mock.puzzle = [
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ]
    assert test.is_end_state(end_state_mock)

    # Some Moves Left, no Eggs
    end_state_mock.puzzle = []

    end_state_mock.moves_left = 1
    assert test.is_end_state(end_state_mock)

    end_state_mock.moves_left = 10**8
    assert test.is_end_state(end_state_mock)

    end_state_mock.puzzle = [
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪺", "🟩", "🟩", "🟩", "🟩", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ]
    end_state_mock.moves_left = 1
    assert test.is_end_state(end_state_mock)

    # Egg/s in the Grid, no Moves Left
    end_state_mock.puzzle = ["🥚"]
    end_state_mock.moves_left = 0
    assert test.is_end_state(end_state_mock)

    end_state_mock.puzzle = ["🥚🥚🥚"]
    end_state_mock.moves_left = 0
    assert test.is_end_state(end_state_mock)

    end_state_mock.puzzle = ["🧱🧱🧱🧱", "🧱🥚🟩🧱", "🧱🟩🟩🧱", "🧱🧱🧱🧱"]
    end_state_mock.moves_left = 0
    assert test.is_end_state(end_state_mock)

    end_state_mock.puzzle = ["🍳🟩🟩", "🥚🥚🥚"]
    end_state_mock.moves_left = 0
    assert test.is_end_state(end_state_mock)

    # Some Moves Left, Egg/s in the Grid
    end_state_mock.puzzle = ["🥚"]
    end_state_mock.moves_left = 10
    assert not test.is_end_state(end_state_mock)

    end_state_mock.moves_left = 100
    assert not test.is_end_state(end_state_mock)

    end_state_mock.puzzle = ["🥚🥚🥚"]
    end_state_mock.moves_left = 10
    assert not test.is_end_state(end_state_mock)

    end_state_mock.puzzle = ["🧱🧱🧱🧱", "🧱🥚🟩🧱", "🧱🟩🟩🧱", "🧱🧱🧱🧱"]
    end_state_mock.moves_left = 10**4
    assert not test.is_end_state(end_state_mock)

    end_state_mock.puzzle = ["🍳🟩🟩", "🥚🥚🥚"]
    end_state_mock.moves_left = 3
    assert not test.is_end_state(end_state_mock)

    end_state_mock.puzzle = [
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ]
    end_state_mock.moves_left = 1
    assert not test.is_end_state(end_state_mock)

    # Edge Case: Negative Moves Left (Should Return True Nevertheless)
    end_state_mock.puzzle = ["🥚"]
    end_state_mock.moves_left = -1
    assert test.is_end_state(end_state_mock)


def test_get_range() -> None:
    # Takes in a DIRECTION -> returns a TUPLE of RANGE objects
    mock_level_data = LevelData(
    rows = 0,
    cols = 0,
    max_moves = 10,
    moves_left = 0, 
    points = [0],
    previous_moves = [],
    current_move = '',
    puzzle = [],
    )
    egg_test = Egg(mock_level_data, Display(mock_level_data))

    mock_level_data_1 = LevelData(
        rows = 4, 
        cols = 8,
        max_moves = 10,
        moves_left = 5,
        points = [0],
        previous_moves = [],
        current_move = '',
        puzzle = [
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ]
        )
    egg_test_1 = Egg(mock_level_data_1, Display(mock_level_data_1))

    mock_level_data_2 = LevelData(
        rows = 5, 
        cols = 5,
        max_moves = 10,
        moves_left = 5,
        points = [0],
        previous_moves = [],
        current_move = '',
        puzzle = [
        ["🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🟩", "🍳", "🟩", "🧱"],
        ["🧱", "🪹", "🥚", "🍳", "🧱"],
        ["🧱", "🪹", "🥚", "🥚", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱"]
        ]
        )
    egg_test_2 = Egg(mock_level_data_2, Display(mock_level_data_2))

    # Left and Up
    assert egg_test.get_range(Dir.LEFT) == range(0, 0)
    assert egg_test.get_range(Dir.FORWARD) == range(0, 0)
    assert egg_test_1.get_range(Dir.LEFT) == range(2)
    assert egg_test_1.get_range(Dir.FORWARD) == range(2)
    assert egg_test_2.get_range(Dir.LEFT) == range(3)
    assert egg_test_2.get_range(Dir.FORWARD) == range(3)


    # Right and Down
    assert egg_test.get_range(Dir.RIGHT) == range(-1, -1, -1)
    assert egg_test.get_range(Dir.BACKWARD) == range(-1, -1, -1)
    assert egg_test_1.get_range(Dir.RIGHT) == range(1, -1, -1)
    assert egg_test_1.get_range(Dir.BACKWARD) == range(1, -1, -1)
    assert egg_test_2.get_range(Dir.RIGHT) == range(2, -1, -1)
    assert egg_test_2.get_range(Dir.BACKWARD) == range(2, -1, -1)

    # EDGE CASES:

    # DIRECTIONS is not of type Dir
    assert not egg_test.get_range((0, 0)) 
    assert not egg_test.get_range((2, 0)) 
    assert not egg_test.get_range((0, 2)) 
    assert not egg_test.get_range((10, 10)) 
    assert not egg_test.get_range((727, 0)) 
    assert not egg_test.get_range((10**8, 10**7)) 
    assert not egg_test.get_range(()) 
    assert not egg_test.get_range('haha') 
    assert not egg_test.get_range([]) 
    assert not egg_test.get_range({}) 

    # DIRECTIONS is attribute of Dir, but they are not defined.
    with pytest.raises(AttributeError):
        assert not egg_test.get_range(rows, cols, Dir.UP) 
        assert not egg_test.get_range(rows, cols, Dir.DOWN) 
        assert not egg_test.get_range(rows, cols, Dir.PASS) 


def test_no_eggs_left() -> None:
    # Takes in a GRID -> returns a BOOL
    assert test.no_eggs_left([])
    assert test.no_eggs_left(["🧱🧱🧱🧱", "🧱🟩🟩🧱", "🧱🟩🟩🧱", "🧱🧱🧱🧱"])

    assert not test.no_eggs_left(["🥚"])
    assert not test.no_eggs_left(["🥚🥚🥚"])
    assert not test.no_eggs_left(["🧱🧱🧱🧱", "🧱🥚🟩🧱", "🧱🟩🟩🧱", "🧱🧱🧱🧱"])

    # Larger Examples:
    assert test.no_eggs_left([
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪺", "🟩", "🟩", "🟩", "🟩", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ])

    assert not test.no_eggs_left([
        ["🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🟩", "🍳", "🟩", "🧱"],
        ["🧱", "🪹", "🥚", "🍳", "🧱"],
        ["🧱", "🪹", "🥚", "🟩", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱"]
        ])

    assert test.no_eggs_left([
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪺", "🟩", "🟩", "🟩", "🟩", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ])
    
    assert not test.no_eggs_left([
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
        ])

    # Using Level 1 as a Test Case: 
    assert not test.no_eggs_left(
        ["🧱🧱🧱🧱🧱🧱🧱🧱", 
         "🧱🪹🪹🟩🟩🥚🥚🧱", 
         "🧱🟩🟩🟩🟩🟩🍳🧱", 
         "🧱🧱🧱🧱🧱🧱🧱🧱"]
         )
    assert not test.no_eggs_left(
        ["🧱🧱🧱🧱🧱🧱🧱🧱", 
         "🧱🪹🪹🥚🟩🟩🟩🧱", 
         "🧱🟩🟩🟩🟩🟩🍳🧱", 
         "🧱🧱🧱🧱🧱🧱🧱🧱"]
         )
    assert not test.no_eggs_left(
        ["🧱🧱🧱🧱🧱🧱🧱🧱", 
         "🧱🪹🪹🟩🟩🟩🟩🧱", 
         "🧱🟩🟩🥚🟩🟩🍳🧱", 
         "🧱🧱🧱🧱🧱🧱🧱🧱"]
         )
    assert not test.no_eggs_left(
        ["🧱🧱🧱🧱🧱🧱🧱🧱",
         "🧱🪹🪹🟩🟩🟩🟩🧱", 
         "🧱🥚🟩🟩🟩🟩🍳🧱", 
         "🧱🧱🧱🧱🧱🧱🧱🧱"]
        )
    assert test.no_eggs_left(
        ["🧱🧱🧱🧱🧱🧱🧱🧱",
         "🧱🪹🪹🟩🟩🟩🟩🧱", 
         "🧱🟩🟩🟩🟩🟩🍳🧱", 
         "🧱🧱🧱🧱🧱🧱🧱🧱"]
        )


# MOCK FUNCTION/S FOR TESTING

# Not really sure if randint is the best for the purpose of testing with random values.
def inbound(n: int) -> int:
    # For egg_test.is_inside, returns an INT inside the bounds of rows or cols.
    return randint(0, n - 1)

def outbound(n: int) -> int:
    # For egg_test.is_inside, returns an INT outside the bounds of rows or cols.
    rand_extra = randint(n, 10**7)
    rand_below = randint(-10**7, -1)

    return choice([rand_extra, rand_below])
