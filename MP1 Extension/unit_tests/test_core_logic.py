import pytest
from random import randint, choice
from game import Game, DisplayManager, Block, Level
from utils import Direction, BlockType, BLOCK_MAP


# The methods with no return or yielded values are NOT unit tested.
# Exceptions are some methods in the Block class.
# Inner functions are also not unit tested.

# CORE LOGIC TESTS


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


class GameBlocks(Game):
    # a subclass created to bypass the initializer
    def __init__(self, grid: list[list[str]], moves = 0):
        self.level_data = LevelForTest(self, grid, moves)
        self.grid: list[list[Block]] = self.level_data.grid
        self.moves: int = self.level_data.max_moves
        self.score: int = 0


def test_move() -> None:
    # Given a DIRECTION and index value, change the position of an EGG
    move_test = GameBlocks([
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🥚", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ])

    # Going Left

    # Going Right

    move_test_2 = GameBlocks([
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ])

    # EDGE CASE: No Movables
    move_test_3 = GameBlocks([
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🟩", "🟩", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ])


def test_on_collision() -> None:
    pass


def test_delete() -> None:
    pass


def test_change_block_to() -> None:
    pass


class LevelCreateBlock(Level):
    def __init__(self, game: Game):
        # same as LevelForTest, just no for loop
        self.movables_positions = []
        self.game: Game = game


class GameCreateBlock(Game):
    # for mocking only
    def __init__(self):
        pass


def test_create_block() -> None:
    mock_create = GameCreateBlock()
    create_block_test = LevelCreateBlock(mock_create)

    # _create_block(char, row, col, self.game)
    block = create_block_test._create_block("🥚", 0, 0, mock_create)
    assert block == Block("Egg", "🥚", BlockType.MOVABLE, 0, 0, mock_create)



# def test_move_eggs() -> None:
#     # Takes in a GRID, DIRECTION, ROWS, COLS, and LEVEL_DATA -> returns
#     # a NEW GRID

#     # I haven't found a better way to test than to keep using a
#     # different copy of mock_level_data_x to create a new instance that
#     # is referentially different to prevent side effects

#     # TEST CASE 1
#     mock_level_data_1 = LevelData(
#         rows = 4, 
#         cols = 8,
#         max_moves = 10,
#         moves_left = 5,
#         points = [0],
#         previous_moves = [],
#         current_move = '',
#         puzzle = [
#         ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
#         ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
#         ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
#         ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
#         ]
#         )

#     rows, cols = mock_level_data_1.rows, mock_level_data_1.cols

#     # Moving Right
#     mock_copy = copy.deepcopy(mock_level_data_1)
#     egg_test_1 = Egg(mock_copy, Display(mock_copy))
#     puzzle = [row[:] for row in mock_level_data_1.puzzle]
#     assert egg_test_1.move_eggs(puzzle, Dir.RIGHT, rows, cols, mock_copy) == [
#     ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
#     ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
#     ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
#     ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
#     ]

#     # Moving Left
#     mock_copy = copy.deepcopy(mock_level_data_1)
#     egg_test_1 = Egg(mock_copy, Display(mock_copy))
#     puzzle = [row[:] for row in mock_level_data_1.puzzle]
#     assert egg_test_1.move_eggs(puzzle, Dir.LEFT, rows, cols, mock_copy) == [
#     ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
#     ["🧱", "🪹", "🪹", "🟩", "🥚", "🥚", "🟩", "🧱"],
#     ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
#     ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
#     ]

#     # Moving Forward/Up
#     mock_copy = copy.deepcopy(mock_level_data_1)
#     egg_test_1 = Egg(mock_copy, Display(mock_copy))
#     puzzle = [row[:] for row in mock_level_data_1.puzzle]
#     assert egg_test_1.move_eggs(puzzle, Dir.FORWARD, rows, cols, mock_copy) == [
#     ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
#     ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"],
#     ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"],
#     ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
#     ]

#     # Moving Backward/Down
#     mock_copy = copy.deepcopy(mock_level_data_1)
#     egg_test_1 = Egg(mock_copy, Display(mock_copy))
#     puzzle = [row[:] for row in mock_level_data_1.puzzle]
#     assert egg_test_1.move_eggs(puzzle, Dir.BACKWARD, rows, cols, mock_copy) == [
#     ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
#     ["🧱", "🪹", "🪹", "🟩", "🟩", "🟩", "🟩", "🧱"],
#     ["🧱", "🟩", "🟩", "🟩", "🟩", "🥚", "🍳", "🧱"],
#     ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
#     ]

#     # TEST CASE 2
#     mock_level_data_2 = LevelData(
#         rows = 5, 
#         cols = 5,
#         max_moves = 10,
#         moves_left = 5,
#         points = [0],
#         previous_moves = [],
#         current_move = '',
#         puzzle = [
#         ["🧱", "🧱", "🧱", "🧱", "🧱"],
#         ["🧱", "🟩", "🍳", "🟩", "🧱"],
#         ["🧱", "🪹", "🥚", "🍳", "🧱"],
#         ["🧱", "🪹", "🥚", "🟩", "🧱"],
#         ["🧱", "🧱", "🧱", "🧱", "🧱"]
#         ]
#         )
#     egg_test_2 = Egg(mock_level_data_2, Display(mock_level_data_2))

#     rows_2, cols_2 = mock_level_data_2.rows, mock_level_data_2.cols

#     # Moving Right
#     mock_copy_2 = copy.deepcopy(mock_level_data_2)
#     egg_test_2 = Egg(mock_copy_2, Display(mock_copy_2))
#     puzzle_2 = [row[:] for row in mock_level_data_2.puzzle]
#     assert egg_test_2.move_eggs(puzzle_2, Dir.RIGHT, rows_2, cols_2, mock_copy_2) == [
#     ["🧱", "🧱", "🧱", "🧱", "🧱"],
#     ["🧱", "🟩", "🍳", "🟩", "🧱"],
#     ["🧱", "🪹", "🟩", "🍳", "🧱"],
#     ["🧱", "🪹", "🟩", "🥚", "🧱"],
#     ["🧱", "🧱", "🧱", "🧱", "🧱"]
#     ]

#     # Moving Left
#     mock_copy_2 = copy.deepcopy(mock_level_data_2)
#     egg_test_2 = Egg(mock_copy_2, Display(mock_copy_2))
#     puzzle_2 = [row[:] for row in mock_level_data_2.puzzle]
#     assert egg_test_2.move_eggs(puzzle_2, Dir.LEFT, rows_2, cols_2, mock_copy_2) == [
#     ["🧱", "🧱", "🧱", "🧱", "🧱"],
#     ["🧱", "🟩", "🍳", "🟩", "🧱"],
#     ["🧱", "🪺", "🟩", "🍳", "🧱"],
#     ["🧱", "🪺", "🟩", "🟩", "🧱"],
#     ["🧱", "🧱", "🧱", "🧱", "🧱"]
#     ]

#     # Moving Forward/Up
#     mock_copy_2 = copy.deepcopy(mock_level_data_2)
#     egg_test_2 = Egg(mock_copy_2, Display(mock_copy_2))
#     puzzle_2 = [row[:] for row in mock_level_data_2.puzzle]
#     assert egg_test_2.move_eggs(puzzle_2, Dir.FORWARD, rows_2, cols_2, mock_copy_2) == [
#     ["🧱", "🧱", "🧱", "🧱", "🧱"],
#     ["🧱", "🟩", "🍳", "🟩", "🧱"],
#     ["🧱", "🪹", "🥚", "🍳", "🧱"],
#     ["🧱", "🪹", "🟩", "🟩", "🧱"],
#     ["🧱", "🧱", "🧱", "🧱", "🧱"]
#     ]

#     # Moving Backward/Down
#     mock_copy_2 = copy.deepcopy(mock_level_data_2)
#     egg_test_2 = Egg(mock_copy_2, Display(mock_copy_2))
#     puzzle_2 = [row[:] for row in mock_level_data_2.puzzle]
#     assert egg_test_2.move_eggs(puzzle_2, Dir.BACKWARD, rows_2, cols_2, mock_copy_2) == [
#     ["🧱", "🧱", "🧱", "🧱", "🧱"],
#     ["🧱", "🟩", "🍳", "🟩", "🧱"],
#     ["🧱", "🪹", "🥚", "🍳", "🧱"],
#     ["🧱", "🪹", "🥚", "🟩", "🧱"],
#     ["🧱", "🧱", "🧱", "🧱", "🧱"]
    # ]

