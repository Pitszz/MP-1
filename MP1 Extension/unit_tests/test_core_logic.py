import pytest
from random import randint, choice
from shadow import Game, Egg, Display, Dir


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
egg_test = Egg({}, Display({}))


def test_move_eggs() -> None:
    # Takes in a GRID, DIRECTION, ROWS, COLS, and LEVEL_DATA -> returns a NEW GRID

    # TEST CASE 1
    grid = [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    rows, cols = 4, 8
    level_data = {
    'moves_left': 5, 
    'points': [0]
    }

    # Moving Right
    dire = Dir.RIGHT
    assert egg_test.move_eggs(grid, dire, rows, cols, level_data) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Moving Left
    dire = Dir.LEFT
    assert egg_test.move_eggs(grid, dire, rows, cols, level_data) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🪹", "🪹", "🟩", "🥚", "🥚", "🟩", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Moving Forward/Up
    dire = Dir.FORWARD
    assert egg_test.move_eggs(grid, dire, rows, cols, level_data) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Moving Backward/Down
    dire = Dir.BACKWARD
    assert egg_test.move_eggs(grid, dire, rows, cols, level_data) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🟩", "🟩", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🥚", "🍳", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]


    # TEST CASE 2
    grid_2 = [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🥚", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    rows_2, cols_2 = 5, 5
    level_data_2 = {
    'moves_left': 10,
    'points': [0]
    }

    # Moving Right
    dire = Dir.RIGHT
    assert egg_test.move_eggs(grid_2, dire, rows_2, cols_2, level_data_2) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🟩", "🍳", "🧱"],
    ["🧱", "🪹", "🟩", "🥚", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Moving Left
    dire = Dir.LEFT
    assert egg_test.move_eggs(grid_2, dire, rows_2, cols_2, level_data_2) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪺", "🟩", "🍳", "🧱"],
    ["🧱", "🪺", "🟩", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Moving Forward/Up
    dire = Dir.FORWARD
    assert egg_test.move_eggs(grid_2, dire, rows_2, cols_2, level_data_2) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🟩", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Moving Backward/Down
    dire = Dir.BACKWARD
    assert egg_test.move_eggs(grid_2, dire, rows_2, cols_2, level_data_2) == [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🥚", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]


def test_get_range() -> None:
    # Takes in a ROWS, COLS, and DIRECTION -> returns a TUPLE of RANGE objects

    # Normal Inputs:
    rows, cols = 10, 10 # ROWS and COLS are equal
    rows_1, cols_1 = 10, 5 # ROWS larger than COLS
    rows_2, cols_2 = 5, 10 # ROWS smaller than COLS

    # Left and Up
    assert egg_test.get_range(rows, cols, Dir.LEFT) == (range(rows), range(cols))
    assert egg_test.get_range(rows, cols, Dir.FORWARD) == (range(rows), range(cols))
    assert egg_test.get_range(rows_1, cols_1, Dir.LEFT) == (range(rows_1), range(cols_1))
    assert egg_test.get_range(rows_1, cols_1, Dir.FORWARD) == (range(rows_1), range(cols_1))
    assert egg_test.get_range(rows_2, cols_2, Dir.LEFT) == (range(rows_2), range(cols_2))
    assert egg_test.get_range(rows_2, cols_2, Dir.FORWARD) == (range(rows_2), range(cols_2))

    # Right and Down
    assert egg_test.get_range(rows, cols, Dir.RIGHT) == (range(rows - 1, -1, -1), range(cols - 1, -1, -1))
    assert egg_test.get_range(rows, cols, Dir.BACKWARD) == (range(cols - 1, -1, -1), range(cols - 1, -1, -1))
    assert egg_test.get_range(rows_1, cols_1, Dir.RIGHT) == (range(rows_1 - 1, -1, -1), range(cols_1 - 1, -1, -1))
    assert egg_test.get_range(rows_1, cols_1, Dir.BACKWARD) == (range(rows_1 - 1, -1, -1), range(cols_1 - 1, -1, -1))
    assert egg_test.get_range(rows_2, cols_2, Dir.RIGHT) == (range(rows_2 - 1, -1, -1), range(cols_2 - 1, -1, -1))
    assert egg_test.get_range(rows_2, cols_2, Dir.BACKWARD) == (range(rows_2 - 1, -1, -1), range(cols_2 - 1, -1, -1))

    # EDGE CASES:

    # DIRECTIONS is not of type Dir
    assert not egg_test.get_range(rows, cols, (0, 0)) 
    assert not egg_test.get_range(rows, cols, (2, 0)) 
    assert not egg_test.get_range(rows, cols, (0, 2)) 
    assert not egg_test.get_range(rows, cols, (10, 10)) 
    assert not egg_test.get_range(rows, cols, (727, 0)) 
    assert not egg_test.get_range(rows, cols, (10**8, 10**7)) 

    # DIRECTIONS is attribute of Dir, but they are not defined.
    with pytest.raises(AttributeError):
        assert not egg_test.get_range(rows, cols, Dir.UP) 
        assert not egg_test.get_range(rows, cols, Dir.DOWN) 
        assert not egg_test.get_range(rows, cols, Dir.PASS) 

    # ROWS or COLS is less than 1 (should still return a TUPLE of RANGES)

    rows, cols = 0, 0 # ROWS and COLS are 0
    rows_1, cols_1 = 10, 0 # COLS is 0
    rows_2, cols_2 = 0, 10 # ROWS is 0
    rows_3, cols_3 = -10, -10 # ROWS and COLS are negative

    # Left and Up
    assert egg_test.get_range(rows, cols, Dir.LEFT) == (range(rows), range(cols))
    assert egg_test.get_range(rows, cols, Dir.FORWARD) == (range(rows), range(cols))
    assert egg_test.get_range(rows_1, cols_1, Dir.LEFT) == (range(rows_1), range(cols_1))
    assert egg_test.get_range(rows_1, cols_1, Dir.FORWARD) == (range(rows_1), range(cols_1))
    assert egg_test.get_range(rows_2, cols_2, Dir.LEFT) == (range(rows_2), range(cols_2))
    assert egg_test.get_range(rows_2, cols_2, Dir.FORWARD) == (range(rows_2), range(cols_2))
    assert egg_test.get_range(rows_3, cols_3, Dir.LEFT) == (range(rows_3), range(cols_3))
    assert egg_test.get_range(rows_3, cols_3, Dir.FORWARD) == (range(rows_3), range(cols_3))

    # Right and Down
    assert egg_test.get_range(rows, cols, Dir.RIGHT) == (range(rows - 1, -1, -1), range(cols - 1, -1, -1))
    assert egg_test.get_range(rows, cols, Dir.BACKWARD) == (range(cols - 1, -1, -1), range(cols - 1, -1, -1))
    assert egg_test.get_range(rows_1, cols_1, Dir.RIGHT) == (range(rows_1 - 1, -1, -1), range(cols_1 - 1, -1, -1))
    assert egg_test.get_range(rows_1, cols_1, Dir.BACKWARD) == (range(rows_1 - 1, -1, -1), range(cols_1 - 1, -1, -1))
    assert egg_test.get_range(rows_2, cols_2, Dir.RIGHT) == (range(rows_2 - 1, -1, -1), range(cols_2 - 1, -1, -1))
    assert egg_test.get_range(rows_2, cols_2, Dir.BACKWARD) == (range(rows_2 - 1, -1, -1), range(cols_2 - 1, -1, -1))
    assert egg_test.get_range(rows_3, cols_3, Dir.RIGHT) == (range(rows_3 - 1, -1, -1), range(cols_3 - 1, -1, -1))
    assert egg_test.get_range(rows_3, cols_3, Dir.BACKWARD) == (range(rows_3 - 1, -1, -1), range(cols_3 - 1, -1, -1))


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
    grid = [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🥚", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    assert egg_test.get_eggs_pos(grid) == [(2, 2), (3, 2)]

    grid = [
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

    assert egg_test.get_eggs_pos(grid) == [(1, 1), (1, 2), (1, 3), (2, 3), (3, 1), (3, 2)]

    grid = [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    assert egg_test.get_eggs_pos(grid) == [(1, 5), (1, 6)]

    # No Eggs
    grid = [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🟩", "🟩", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    assert egg_test.get_eggs_pos(grid) == []

    # Edge Case: Empty GRID
    grid = []
    assert egg_test.get_eggs_pos(grid) == []


    # Edge Case: GRID is a TUPLE[TUPLE[STR]]
    grid = (
    ("🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"), 
    ("🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"), 
    ("🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"), 
    ("🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱")
    )

    assert egg_test.get_eggs_pos(grid) == [(1, 5), (1, 6)]
    

def test_all_eggs_blocked() -> None:
    # Takes in a DICT containing the current PUZZLE, ROWS, COLS; and a DIRECTION -> returns a BOOL

    grid = [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🥚", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Moving Right
    dire = Dir.RIGHT
    assert not egg_test.all_eggs_blocked({"puzzle": grid, "rows": 5, "cols": 5}, dire)


    grid = [
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

    # Moving Left   
    dire = Dir.LEFT
    assert egg_test.all_eggs_blocked({"puzzle": grid, "rows": 9, "cols": 9}, dire)


    grid = [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Moving Forward
    dire = Dir.FORWARD
    assert egg_test.all_eggs_blocked({"puzzle": grid, "rows": 4, "cols": 8}, dire)


    grid = [
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

    # Moving Backward
    dire = Dir.BACKWARD
    assert not egg_test.all_eggs_blocked({"puzzle": grid, "rows": 19, "cols": 19}, dire) 


def test_is_end_state() -> None:
    # Takes in a DICT containing the GRID and MOVES_LEFT -> returns a BOOL

    # No Egg/s Left, No Moves Left
    assert test.is_end_state({"puzzle": [], "moves_left": 0})
    assert test.is_end_state({
        "puzzle": ["🧱🧱🧱🧱", "🧱🟩🟩🧱", "🧱🟩🟩🧱", "🧱🧱🧱🧱"], 
        "moves_left": 0}
        )
    assert test.is_end_state({
        "puzzle": ["🧱🧱🧱🧱", "🧱🪺🟩🧱", "🧱🟩🍳🧱", "🧱🧱🧱🧱"], 
        "moves_left": 0}
        )
    assert test.is_end_state({
        "puzzle": [
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ], 
        "moves_left": 0})

    # Some Moves Left, no Eggs
    assert test.is_end_state({"puzzle": [], "moves_left": 1})
    assert test.is_end_state({"puzzle": [], "moves_left": 10**8})
    assert test.is_end_state({
        "puzzle": [
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪺", "🟩", "🟩", "🟩", "🟩", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ], 
        "moves_left": 1})

    # Egg/s in the Grid, no Moves Left
    assert test.is_end_state({"puzzle": ["🥚"], "moves_left": 0})
    assert test.is_end_state({"puzzle": ["🥚🥚🥚"], "moves_left": 0})
    assert test.is_end_state({
        "puzzle": ["🧱🧱🧱🧱", "🧱🥚🟩🧱", "🧱🟩🟩🧱", "🧱🧱🧱🧱"], 
        "moves_left": 0}
        )

    assert test.is_end_state({"puzzle": ["🍳🟩🟩", "🥚🥚🥚"], "moves_left": 0})

    # Some Moves Left, Egg/s in the Grid
    assert not test.is_end_state({"puzzle": ["🥚"], "moves_left": 10})
    assert not test.is_end_state({"puzzle": ["🥚"], "moves_left": 100})
    assert not test.is_end_state({"puzzle": ["🥚🥚🥚"], "moves_left": 10})
    assert not test.is_end_state({
        "puzzle": ["🧱🧱🧱🧱", "🧱🥚🟩🧱", "🧱🟩🟩🧱", "🧱🧱🧱🧱"], 
        "moves_left": 10**4}
        )

    assert not test.is_end_state({"puzzle": ["🍳🟩🟩", "🥚🥚🥚"], "moves_left": 3})

    assert not test.is_end_state({
        "puzzle": [
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ], 
        "moves_left": 1})

    # Edge Case: Negative Moves Left (Should Return True Nevertheless)
    assert test.is_end_state({"puzzle": ["🥚"], "moves_left": -1})


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
