import pytest
from random import randint, choice
import copy
from game import Game, DisplayManager, Block, Level
from utils import Direction, BlockType


# The methods with no return or yielded values are NOT unit tested.
# Exceptions are some methods in the Block class.
# Inner functions are also not unit tested.

# GAME STATE TESTS


class LevelForTest(Level):
    # a subclass created to bypass _load_level in Level
    def __init__(self, game: Game, grid_test: list[list[str]], max_moves = 0):
        self.grid: list[list[Block]] = []
        self.rows = len(grid_test)
        self.max_moves: int = max_moves

        try:
            self.cols: int = len(grid_test[0])
        except IndexError:
            self.cols = 0

        self.game: Game = game
        self.movables_positions: list[tuple] = []

        for row in range(self.rows):
            line = grid_test[row]
            grid_row = [
                self._create_block(char, row, col, self.game)
                for (col, char) in enumerate(line)
                ]
            self.grid.append(grid_row)


class GameIsInside(Game):
    # a subclass created to use a modified initializer
    def __init__(self, grid: list[list[str]], moves = 0):
        self.level_data = LevelForTest(self, grid, moves)
        self.grid: list[list[Block]] = self.level_data.grid   


def test_is_inside() -> None:
    # Takes in NEW_ROW, NEW_COL, ROWS, and COLS -> returns a BOOL
    is_inside_test = GameIsInside([
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🥚", "🥚", "🥚", "🧱", "🍳", "🟩", "🟩", "🟩", "🧱"],
        ["🧱", "🟩", "🧱", "🥚", "🧱", "🟩", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🥚", "🥚", "🟩", "🪹", "🪹", "🪹", "🟩", "🟩", "🧱"],
        ["🧱", "🟩", "🧱", "🧱", "🧱", "🟩", "🟩", "🟩","🪹", "🧱"],
        ["🧱", "🟩", "🍳", "🟩", "🟩", "🟩", "🟩", "🟩", "🪹", "🧱"],
        ["🧱", "🟩", "🍳", "🟩", "🧱", "🪹", "🍳", "🟩", "🟩", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🍳", "🟩", "🟩", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🍳", "🟩", "🟩", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ])
    rows = is_inside_test.level_data.rows
    cols = is_inside_test.level_data.cols

    print(is_inside_test.grid[2][1]._type)

    assert is_inside_test.is_inside(2, 1, rows, cols)
    assert is_inside_test.is_inside(4, 1, rows, cols)
    assert not is_inside_test.is_inside(1, 0, rows, cols)
    assert not is_inside_test.is_inside(2, 2, rows, cols)
    assert is_inside_test.is_inside(5, 2, rows, cols)
    # even though the pan isn't beside a movable, it is movable to
    assert not is_inside_test.is_inside(10, 10, rows, cols)
    assert not is_inside_test.is_inside(-1, 0, rows, cols)
    assert not is_inside_test.is_inside(0, -1, rows, cols)
    assert not is_inside_test.is_inside(11, 0, rows, cols)
    assert not is_inside_test.is_inside(7, 10**8, rows, cols)

    # EDGE CASES 

    # ROWS or COLS is 0 (Should evaluate to False since 0 < 0)
    rows, cols = 10, 10
    rows_0, cols_0 = 0, 0

    assert not is_inside_test.is_inside(0, 6, rows_0, cols)
    assert not is_inside_test.is_inside(4, 0, rows, cols_0)
    assert not is_inside_test.is_inside(0, 0, rows_0, cols_0)

    # Really Large ROWS and COLS with outbound neighbor, Random Cases
    # inbound test breaks due to the way is_inside is set up
    rows, cols = randint(0, 10**6), randint(0, 10**6)
    in_i, in_j = inbound(rows), inbound(cols)
    out_i, out_j = outbound(rows), outbound(cols)

    assert not is_inside_test.is_inside(in_i, out_j, rows, cols)
    assert not is_inside_test.is_inside(out_i, in_j, rows, cols)
    assert not is_inside_test.is_inside(out_i, out_j, rows, cols)


class GameMovableTo(Game):
    # a subclass created to use a modified initializer
    def __init__(self, grid: list[list[str]], moves = 0):
        self.level_data = LevelForTest(self, grid, moves)
        self.grid: list[list[Block]] = self.level_data.grid


def test_is_movable_to() -> None:
    # takes in a BLOCK, returns a BOOL
    is_movable_test = GameMovableTo([])
    # just need a mock object to test this

    neighbor = Block("Egg", "🥚", BlockType.MOVABLE, 0, 0, is_movable_test)
    assert not is_movable_test.is_movable_to(neighbor)

    neighbor_2 = Block("Grass", "🟩", BlockType.FLOOR, 0, 0, is_movable_test)
    assert is_movable_test.is_movable_to(neighbor_2)

    neighbor_3 = Block("Wall", "🧱", BlockType.IMMOVABLE, 0, 0, is_movable_test)
    assert not is_movable_test.is_movable_to(neighbor_3)

    neighbor_4 = Block("Nest", "🪹", BlockType.GOAL, 0, 0, is_movable_test)
    assert is_movable_test.is_movable_to(neighbor_4)

    neighbor_5 = Block("Full Nest", "🪺", BlockType.IMMOVABLE, 0, 0, is_movable_test)
    assert not is_movable_test.is_movable_to(neighbor_5)

    neighbor_6 = Block("Pan", "🍳", BlockType.VOID, 0, 0, is_movable_test)
    assert is_movable_test.is_movable_to(neighbor_6)

    neighbor_7 = Block("Hole", " ", BlockType.VOID, 0, 0, is_movable_test)
    assert is_movable_test.is_movable_to(neighbor_7)


    # EDGE CASE: Block mismatch
    # Dependent on BlockType, not any other attributes
    neighbor_x = Block("Egg", "🥚", BlockType.FLOOR, 0, 0, is_movable_test)
    assert is_movable_test.is_movable_to(neighbor_x)

    neighbor_y = Block("Pan", "🥚", BlockType.MOVABLE, 0, 0, is_movable_test)
    assert not is_movable_test.is_movable_to(neighbor_y)

    neighbor_z = Block("Egg", "🪹", BlockType.MOVABLE, 0, 0, is_movable_test)
    assert not is_movable_test.is_movable_to(neighbor_z)


    # EDGE CASE: Raises an AttributeError (BlockType nonexistent)
    with pytest.raises(AttributeError):
        neighbor_a = Block("Egg", "🥚", BlockType.FLOORS, 0, 0, is_movable_test)
        assert is_movable_test.is_movable_to(neighbor_a)

        neighbor_b = Block("Egg", "🥚", BlockType.CAR, 0, 0, is_movable_test)
        assert is_movable_test.is_movable_to(neighbor_b)

        neighbor_c = Block("Egg", "🥚", BlockType.FLAG, 0, 0, is_movable_test)
        assert is_movable_test.is_movable_to(neighbor_c)

        neighbor_d = Block("Egg", "🥚", BlockType.TYPE, 0, 0, is_movable_test)
        assert is_movable_test.is_movable_to(neighbor_d)


class GameMovablesPos(Game):
    # a subclass created to use a modified initializer
    def __init__(self, grid: list[list[str]], moves = 0):
        self.level_data = LevelForTest(self, grid, moves)


def test_get_eggs_pos() -> None:
    # Tests if movables_positions is filled up correctly.

    movables_test = GameMovablesPos([
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🥚", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    assert movables_test.level_data.movables_positions == [(2, 2), (3, 2)]

    movables_test_2 = GameMovablesPos([
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🥚", "🥚", "🥚", "🧱", "🍳", "🟩", "🟩", "🧱"],
    ["🧱", "🟩", "🧱", "🥚", "🧱", "🟩", "🧱", "🧱", "🧱"],
    ["🧱", "🥚", "🥚", "🟩", "🪹", "🪹", "🪹", "🟩", "🧱"],
    ["🧱", "🟩", "🧱", "🧱", "🧱", "🟩", "🟩", "🪹", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🟩", "🟩", "🟩", "🪹", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱", "🪹", "🍳", "🟩", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    assert movables_test_2.level_data.movables_positions == [(1, 1), (1, 2), (1, 3), (2, 3), (3, 1), (3, 2)]

    movables_test_3 = GameMovablesPos([
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    assert movables_test_3.level_data.movables_positions == [(1, 5), (1, 6)]

    # No Eggs
    movables_test_4 = GameMovablesPos([
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🟩", "🟩", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    assert movables_test_4.level_data.movables_positions == []

    # Edge Case: Empty GRID
    movables_test_5 = GameMovablesPos([])
    assert movables_test_5.level_data.movables_positions == []

    # Edge Case: GRID is a TUPLE[TUPLE[STR]]
    movables_test_6 = GameMovablesPos((
    ("🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"), 
    ("🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"), 
    ("🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"), 
    ("🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱")
    ))

    assert movables_test_6.level_data.movables_positions == [(1, 5), (1, 6)]
    

class GameObjectsBlocked(Game):
    # a subclass created to use a modified initializer
    def __init__(self, grid: list[list[str]], moves = 0):
        self.level_data = LevelForTest(self, grid, moves)
        self.grid: list[list[Block]] = self.level_data.grid
        self.moves = self.level_data.max_moves


def test_all_objects_blocked() -> None:
    # Takes in ROWS, COLS and a DIRECTION -> returns a BOOL
    
    # Moving Right
    eggs_blocked_test = GameObjectsBlocked([
        ["🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🟩", "🍳", "🟩", "🧱"],
        ["🧱", "🪹", "🥚", "🍳", "🧱"],
        ["🧱", "🪹", "🥚", "🟩", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱"]
        ])
    rows = eggs_blocked_test.level_data.rows
    cols = eggs_blocked_test.level_data.cols

    assert not eggs_blocked_test.all_objects_blocked(rows, cols, Direction.RIGHT)

    # Moving Left  
    eggs_blocked_test_2 = GameObjectsBlocked([
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🥚", "🥚", "🥚", "🧱", "🍳", "🟩", "🟩", "🧱"],
    ["🧱", "🟩", "🧱", "🥚", "🧱", "🟩", "🧱", "🧱", "🧱"],
    ["🧱", "🥚", "🥚", "🟩", "🪹", "🪹", "🪹", "🟩", "🧱"],
    ["🧱", "🟩", "🧱", "🧱", "🧱", "🟩", "🟩", "🪹", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🟩", "🟩", "🟩", "🪹", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱", "🪹", "🍳", "🟩", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    rows = eggs_blocked_test_2.level_data.rows
    cols = eggs_blocked_test_2.level_data.cols

    assert eggs_blocked_test_2.all_objects_blocked(rows, cols, Direction.LEFT)

    # Moving Forward
    eggs_blocked_test_3 = GameObjectsBlocked([
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    rows = eggs_blocked_test_3.level_data.rows
    cols = eggs_blocked_test_3.level_data.cols

    assert eggs_blocked_test_3.all_objects_blocked(rows, cols, Direction.FORWARD)


    # Moving Backward
    eggs_blocked_test_4 = GameObjectsBlocked([
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
    rows = eggs_blocked_test_4.level_data.rows
    cols = eggs_blocked_test_4.level_data.cols

    assert not eggs_blocked_test_4.all_objects_blocked(rows, cols, Direction.BACKWARD) 

    # EDGE CASE: Grid passed is empty
    eggs_blocked_test_x = GameObjectsBlocked([])
    rows = eggs_blocked_test_x.level_data.rows
    cols = eggs_blocked_test_x.level_data.cols

    assert eggs_blocked_test_x.all_objects_blocked(rows, cols, Direction.LEFT) 
    # returns True by technicality since it's based on the amount of MOVABLES


class GameEndState(Game):
    # a subclass created to use a modified initializer
    def __init__(self, grid: list[list[str]], moves = 0):
        self.level_data = LevelForTest(self, grid, moves)
        self.grid: list[list[Block]] = self.level_data.grid
        self.moves = self.level_data.max_moves


def test_is_end_state() -> None:
    # Takes in a GRID and MOVES -> returns a BOOL

    # No Egg/s Left, No Moves Left
    end_state_test = GameEndState([])
    assert end_state_test.is_end_state()

    end_state_test_2 = GameEndState([
        ['🧱', '🧱', '🧱', '🧱'],
        ['🧱', '🟩', '🟩', '🧱'],
        ['🧱', '🟩', '🟩', '🧱'],
        ['🧱', '🧱', '🧱', '🧱']
        ])
    assert end_state_test_2.is_end_state()

    end_state_test_3 = GameEndState([
        ['🧱', '🧱', '🧱', '🧱'],
        ['🧱', '🪺', '🟩', '🧱'],
        ['🧱', '🟩', '🍳', '🧱'],
        ['🧱', '🧱', '🧱', '🧱']
        ])
    assert end_state_test_3.is_end_state()

    end_state_test_4 = GameEndState([
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ])
    assert end_state_test_4.is_end_state()

    # Some Moves Left, no Eggs
    end_state_test_5 = GameEndState([], 1)
    assert end_state_test_5.is_end_state()

    end_state_test_6 = GameEndState([], 10**8)
    assert end_state_test_6.is_end_state()

    end_state_test_7 = GameEndState([
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪺", "🟩", "🟩", "🟩", "🟩", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ], 1)
    assert end_state_test_7.is_end_state()

    # Egg/s in the Grid, no Moves Left
    end_state_test_8 = GameEndState(["🥚"])
    assert end_state_test_8.is_end_state()

    end_state_test_9 = GameEndState(["🥚", "🥚", "🥚"])
    assert end_state_test_9.is_end_state()

    end_state_test_10 = GameEndState([
        ["🧱", "🧱", "🧱", "🧱"], 
        ["🧱", "🥚", "🟩", "🧱"], 
        ["🧱", "🟩", "🟩", "🧱"], 
        ["🧱", "🧱", "🧱", "🧱"]
        ])
    assert end_state_test_10.is_end_state()

    end_state_test_11 = GameEndState([
        ["🍳", "🟩", "🟩"], 
        ["🥚", "🥚", "🥚"]
        ])
    assert end_state_test_11.is_end_state()

    # Some Moves Left, Egg/s in the Grid
    end_state_test_12 = GameEndState(["🥚"], 10)
    assert not end_state_test_12.is_end_state()

    end_state_test_13 = GameEndState(["🥚"], 100)
    assert not end_state_test_13.is_end_state()

    end_state_test_14 = GameEndState(["🥚", "🥚", "🥚"], 10)
    assert not end_state_test_14.is_end_state()

    end_state_test_15 = GameEndState([
        ["🧱", "🧱", "🧱", "🧱"], 
        ["🧱", "🥚", "🟩", "🧱"], 
        ["🧱", "🟩", "🟩", "🧱"], 
        ["🧱", "🧱", "🧱", "🧱"]], 10**4)
    assert not end_state_test_15.is_end_state()

    end_state_test_16 = GameEndState([
        ["🍳", "🟩", "🟩"], 
        ["🥚", "🥚", "🥚"]
        ], 3)
    assert not end_state_test_16.is_end_state()

    end_state_test_17 = GameEndState([
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ], 1)
    assert not end_state_test_17.is_end_state()

    # Edge Case: Negative Moves Left (Should Return True Nevertheless)
    end_state_test_x = GameEndState(["🥚"], -1)
    assert end_state_test_x.is_end_state()


class GameGetRange(Game):
    # a subclass created to use a modified initializer
    def __init__(self, grid: list[list[str]]):
        self.level_data = LevelForTest(self, grid)
        self.grid: list[list[Block]] = self.level_data.grid


def test_get_range() -> None:
    # Takes in a DIRECTION -> returns a RANGE
    get_range_test = GameGetRange([])
    get_range_test_2 = GameGetRange([
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ])
    get_range_test_3 = GameGetRange([
        ["🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🟩", "🍳", "🟩", "🧱"],
        ["🧱", "🪹", "🥚", "🍳", "🧱"],
        ["🧱", "🪹", "🥚", "🥚", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱"]
        ])

    # Left and Up
    assert get_range_test.get_range(Direction.LEFT) == range(0, 0)
    assert get_range_test.get_range(Direction.FORWARD) == range(0, 0)
    assert get_range_test_2.get_range(Direction.LEFT) == range(2)
    assert get_range_test_2.get_range(Direction.FORWARD) == range(2)
    assert get_range_test_3.get_range(Direction.LEFT) == range(3)
    assert get_range_test_3.get_range(Direction.FORWARD) == range(3)


    # Right and Down
    assert get_range_test.get_range(Direction.RIGHT) == range(-1, -1, -1)
    assert get_range_test.get_range(Direction.BACKWARD) == range(-1, -1, -1)
    assert get_range_test_2.get_range(Direction.RIGHT) == range(1, -1, -1)
    assert get_range_test_2.get_range(Direction.BACKWARD) == range(1, -1, -1)
    assert get_range_test_3.get_range(Direction.RIGHT) == range(2, -1, -1)
    assert get_range_test_3.get_range(Direction.BACKWARD) == range(2, -1, -1)

    # EDGE CASES:

    # DIRECTIONS is not of type Dir
    assert not get_range_test.get_range((0, 0)) 
    assert not get_range_test.get_range((2, 0)) 
    assert not get_range_test.get_range((0, 2)) 
    assert not get_range_test.get_range((10, 10)) 
    assert not get_range_test.get_range((727, 0)) 
    assert not get_range_test.get_range((10**8, 10**7)) 
    assert not get_range_test.get_range(()) 
    assert not get_range_test.get_range('haha') 
    assert not get_range_test.get_range([]) 
    assert not get_range_test.get_range({}) 

    # DIRECTIONS is attribute of Dir, but they are not defined.
    with pytest.raises(AttributeError):
        assert not get_range_test.get_range(Direction.UP) 
        assert not get_range_test.get_range(Direction.DOWN) 
        assert not get_range_test.get_range(Direction.PASS) 


class GameNoMovables(Game):
    # a subclass created to use a modified initializer
    def __init__(self, grid: list[list[str]]):
        self.level_data = LevelForTest(self, grid)
        self.grid: list[list[Block]] = self.level_data.grid


def test_no_movables_left() -> None:
    # Takes in a GRID -> returns a BOOL

    no_movables_test = GameNoMovables([])
    assert no_movables_test.no_movables_left()

    no_movables_test_2 = GameNoMovables([
        ['🧱', '🧱', '🧱', '🧱'],
        ['🧱', '🟩', '🟩', '🧱'],
        ['🧱', '🟩', '🟩', '🧱'],
        ['🧱', '🧱', '🧱', '🧱']
        ])
    assert no_movables_test_2.no_movables_left()

    no_movables_test_3 = GameNoMovables(['🥚'])
    assert not no_movables_test_3.no_movables_left()

    no_movables_test_4 = GameNoMovables(['🥚', '🥚', '🥚'])
    assert not no_movables_test_4.no_movables_left()

    no_movables_test_5 = GameNoMovables([
        ['🧱', '🧱', '🧱', '🧱'],
        ['🧱', '🥚', '🟩', '🧱'],
        ['🧱', '🟩', '🟩', '🧱'],
        ['🧱', '🧱', '🧱', '🧱']
        ])
    assert not no_movables_test_5.no_movables_left()

    # Larger Examples:
    no_movables_test_6 = GameNoMovables([
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪺", "🟩", "🟩", "🟩", "🟩", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ])
    assert no_movables_test_6.no_movables_left()

    no_movables_test_7 = GameNoMovables([
        ["🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🟩", "🍳", "🟩", "🧱"],
        ["🧱", "🪹", "🥚", "🍳", "🧱"],
        ["🧱", "🪹", "🥚", "🟩", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱"]
        ])
    assert not no_movables_test_7.no_movables_left()

    no_movables_test_8 = GameNoMovables([
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ["🧱", "🪹", "🪺", "🟩", "🟩", "🟩", "🟩", "🧱"],
        ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
        ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
        ])
    assert no_movables_test_8.no_movables_left()
    
    no_movables_test_9 = GameNoMovables([
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
    assert not no_movables_test_9.no_movables_left()

    # Using Level 1 as a Test Case: 
    no_movables_test_a = GameNoMovables(
        ["🧱🧱🧱🧱🧱🧱🧱🧱", 
         "🧱🪹🪹🟩🟩🥚🥚🧱", 
         "🧱🟩🟩🟩🟩🟩🍳🧱", 
         "🧱🧱🧱🧱🧱🧱🧱🧱"]
         )
    assert not no_movables_test_a.no_movables_left()

    no_movables_test_b = GameNoMovables(
        ["🧱🧱🧱🧱🧱🧱🧱🧱", 
         "🧱🪹🪹🥚🟩🟩🟩🧱", 
         "🧱🟩🟩🟩🟩🟩🍳🧱", 
         "🧱🧱🧱🧱🧱🧱🧱🧱"]
         )
    assert not no_movables_test_b.no_movables_left()

    no_movables_test_c = GameNoMovables(
        ["🧱🧱🧱🧱🧱🧱🧱🧱", 
         "🧱🪹🪹🟩🟩🟩🟩🧱", 
         "🧱🟩🟩🥚🟩🟩🍳🧱", 
         "🧱🧱🧱🧱🧱🧱🧱🧱"]
         )
    assert not no_movables_test_c.no_movables_left()

    no_movables_test_d = GameNoMovables(
        ["🧱🧱🧱🧱🧱🧱🧱🧱",
         "🧱🪹🪹🟩🟩🟩🟩🧱", 
         "🧱🥚🟩🟩🟩🟩🍳🧱", 
         "🧱🧱🧱🧱🧱🧱🧱🧱"]
         )
    assert not no_movables_test_d.no_movables_left()

    no_movables_test_e = GameNoMovables(
        ["🧱🧱🧱🧱🧱🧱🧱🧱",
         "🧱🪹🪹🟩🟩🟩🟩🧱", 
         "🧱🟩🟩🟩🟩🟩🍳🧱", 
         "🧱🧱🧱🧱🧱🧱🧱🧱"]
         )
    assert no_movables_test_e.no_movables_left()


# MOCK FUNCTION/S FOR TESTING

# Not really sure if randint is the best for the purpose of testing with random values.
def inbound(n: int) -> int:
    # For is_inside_test.is_inside, returns an INT inside the bounds of rows or cols.
    return randint(0, n - 1)

def outbound(n: int) -> int:
    # For is_inside_test.is_inside, returns an INT outside the bounds of rows or cols.
    rand_extra = randint(n, 10**7)
    rand_below = randint(-10**7, -1)

    return choice([rand_extra, rand_below])