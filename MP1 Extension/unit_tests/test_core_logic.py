import pytest
from game import Game, DisplayManager, Block, Level
from utils import Direction, BlockType, Sprite


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
        self.remove_movables: list[int] = []


class GameCreateBlock(Game):
    # for mocking Block creation
    def __init__(self):
        self.score: int = 0
        pass


class LevelCreateBlock(Level):
    def __init__(self, game: Game):
        # modified Level class for creating Blocks
        self.movables_positions = []
        self.game: Game = game


def test_move() -> None:
    # Given a DIRECTION, change the position of MOVABLES

    # TEST CASE 1
    move_test_a = GameBlocks([
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🥚", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    assert move_test_a.level_data.movables_positions == [(2, 2), (3, 2)]

    # Going Left
    direction = Direction.LEFT
    for x in move_test_a.get_range(direction):
        i, j = move_test_a.level_data.movables_positions[x]
        block = move_test_a.grid[i][j]
        assert block._type == BlockType.MOVABLE
        block.move(direction, x)

    grid_left = [[block.sprite for block in row] for row in move_test_a.level_data.grid]

    assert grid_left == [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪺", "🟩", "🍳", "🧱"],
    ["🧱", "🪺", "🟩", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Going Right
    move_test_b = GameBlocks([
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🥚", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    assert move_test_b.level_data.movables_positions == [(2, 2), (3, 2)]

    direction = Direction.RIGHT
    for x in move_test_b.get_range(direction):
        i, j = move_test_b.level_data.movables_positions[x]
        block = move_test_b.grid[i][j]
        assert block._type == BlockType.MOVABLE
        block.move(direction, x)

    grid_right = [[block.sprite for block in row] for row in move_test_b.level_data.grid]

    assert grid_right == [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🟩", "🍳", "🧱"],
    ["🧱", "🪹", "🟩", "🥚", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Going Forward
    move_test_c = GameBlocks([
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🥚", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    assert move_test_c.level_data.movables_positions == [(2, 2), (3, 2)]

    direction = Direction.FORWARD
    for x in move_test_c.get_range(direction):
        i, j = move_test_c.level_data.movables_positions[x]
        block = move_test_c.grid[i][j]
        assert block._type == BlockType.MOVABLE
        block.move(direction, x)

    grid_forward = [[block.sprite for block in row] for row in move_test_c.level_data.grid]

    assert grid_forward == [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🟩", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # Going Backward
    move_test_d = GameBlocks([
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🥚", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    assert move_test_d.level_data.movables_positions == [(2, 2), (3, 2)]

    direction = Direction.BACKWARD
    for x in move_test_d.get_range(direction):
        i, j = move_test_d.level_data.movables_positions[x]
        block = move_test_d.grid[i][j]
        assert block._type == BlockType.MOVABLE
        block.move(direction, x)

    grid_backward = [[block.sprite for block in row] for row in move_test_d.level_data.grid]

    assert grid_backward == [
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🥚", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # TEST CASE 2
    move_test_2a = GameBlocks([
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    assert move_test_2a.level_data.movables_positions == [(1, 5), (1, 6)]

    # Going Left
    direction = Direction.LEFT
    for x in move_test_2a.get_range(direction):
        i, j = move_test_2a.level_data.movables_positions[x]
        block = move_test_2a.grid[i][j]
        assert block._type == BlockType.MOVABLE
        block.move(direction, x)

    grid2_left = [[block.sprite for block in row] for row in move_test_2a.level_data.grid]

    assert grid2_left == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🥚", "🥚", "🟩", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    move_test_2b = GameBlocks([
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    assert move_test_2b.level_data.movables_positions == [(1, 5), (1, 6)]

    # Going Right
    direction = Direction.RIGHT
    for x in move_test_2b.get_range(direction):
        i, j = move_test_2b.level_data.movables_positions[x]
        block = move_test_2b.grid[i][j]
        assert block._type == BlockType.MOVABLE
        block.move(direction, x)

    grid2_right = [[block.sprite for block in row] for row in move_test_2b.level_data.grid]

    assert grid2_right == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    move_test_2c = GameBlocks([
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    assert move_test_2c.level_data.movables_positions == [(1, 5), (1, 6)]

    # Going Forward
    direction = Direction.FORWARD
    for x in move_test_2c.get_range(direction):
        i, j = move_test_2c.level_data.movables_positions[x]
        block = move_test_2c.grid[i][j]
        assert block._type == BlockType.MOVABLE
        block.move(direction, x)

    grid2_forward = [[block.sprite for block in row] for row in move_test_2c.level_data.grid]

    assert grid2_forward == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    move_test_2d = GameBlocks([
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🥚", "🥚", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    assert move_test_2d.level_data.movables_positions == [(1, 5), (1, 6)]

    # Going Backward
    direction = Direction.BACKWARD
    for x in move_test_2d.get_range(direction):
        i, j = move_test_2d.level_data.movables_positions[x]
        block = move_test_2d.grid[i][j]
        assert block._type == BlockType.MOVABLE
        block.move(direction, x)

    grid2_backward = [[block.sprite for block in row] for row in move_test_2d.level_data.grid]

    assert grid2_backward == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🟩", "🟩", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🥚", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # EDGE CASE: No Movables
    move_test_x = GameBlocks([
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🟩", "🟩", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    assert move_test_x.level_data.movables_positions == []

    direction = Direction.LEFT
    for x in move_test_x.get_range(direction):
        i, j = move_test_x.level_data.movables_positions[x]
        block = move_test_x.grid[i][j]
        assert block._type == BlockType.MOVABLE
        block.move(direction, x)

    grid_x = [[block.sprite for block in row] for row in move_test_x.level_data.grid]
    assert grid_x == [
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"], 
    ["🧱", "🪹", "🪹", "🟩", "🟩", "🟩", "🟩", "🧱"], 
    ["🧱", "🟩", "🟩", "🟩", "🟩", "🟩", "🍳", "🧱"], 
    ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"]
    ]

    # EDGE CASE: Undefined Direction
    move_test_y = GameBlocks([
    ["🧱", "🧱", "🧱", "🧱", "🧱"],
    ["🧱", "🟩", "🍳", "🟩", "🧱"],
    ["🧱", "🪹", "🥚", "🍳", "🧱"],
    ["🧱", "🪹", "🥚", "🟩", "🧱"],
    ["🧱", "🧱", "🧱", "🧱", "🧱"]
    ])
    assert move_test_d.level_data.movables_positions == [(2, 2), (3, 2)]

    with pytest.raises(AttributeError): 
        assert move_test_y.grid[2][2].move(Direction.NULL, 0) 
        assert move_test_y.grid[2][2].move(Direction.FLAG, 0) 
        assert move_test_y.grid[3][2].move(Direction.WRONG, 1) 


def test_on_collision() -> None:
    # Tests if MOVABLE at a given index can move onto neighbor
    
    # Test Cases: using a new instance of mock_collision every time

    # FLOOR Collision
    mock_collision = GameBlocks(["🥚"])  # so movable_positions is True
    collision_test = LevelCreateBlock(mock_collision)

    floor_collision = collision_test._create_block("🥚", 0, 0, mock_collision)
    neighbor_floor = collision_test._create_block("🟩", 0, 1, mock_collision)
    assert neighbor_floor._type.name == BlockType.FLOOR.name

    floor_collision.new_row = floor_collision.row + neighbor_floor.row
    floor_collision.new_col = floor_collision.col + neighbor_floor.col
    floor_collision.on_collision(neighbor_floor, 0)
    assert floor_collision.sprite == "🟩"
    assert neighbor_floor.sprite == "🥚"

    # VOID Collision
    mock_collision = GameBlocks(["🥚"])  # so movable_positions is True
    collision_test = LevelCreateBlock(mock_collision)

    void_collision = collision_test._create_block("🥚", 0, 0, mock_collision)
    neighbor_void = collision_test._create_block("🍳", 1, 0, mock_collision)
    assert neighbor_void._type.name == BlockType.VOID.name

    void_collision.new_row = void_collision.row + neighbor_void.row
    void_collision.new_col = void_collision.col + neighbor_void.col
    void_collision.on_collision(neighbor_void, 0)
    assert void_collision.sprite == "🟩"
    assert neighbor_void.sprite == "🍳"
    assert mock_collision.score == -5

    # GOAL Collision
    mock_collision = GameBlocks(["🥚"])  # so movable_positions is True
    collision_test = LevelCreateBlock(mock_collision)

    goal_collision = collision_test._create_block("🥚", 0, 0, mock_collision)
    neighbor_goal = collision_test._create_block("🪹", -1, 0, mock_collision)
    assert neighbor_goal._type.name == BlockType.GOAL.name

    goal_collision.new_row = goal_collision.row + neighbor_goal.row
    goal_collision.new_col = goal_collision.col + neighbor_goal.col
    goal_collision.on_collision(neighbor_goal, 0)
    assert goal_collision.sprite == "🟩"
    assert neighbor_goal.sprite == "🪺"
    assert mock_collision.score == 10 + 1  # current move counted

    # MOVABLE OR IMMOVABLE Collision (they act the same)
    mock_collision = GameBlocks(["🥚"])  # so movable_positions is True
    collision_test = LevelCreateBlock(mock_collision)

    move_collision = collision_test._create_block("🥚", 0, 0, mock_collision)
    neighbor_move = collision_test._create_block("🥚", 0, -1, mock_collision)
    assert neighbor_move._type.name == BlockType.MOVABLE.name

    # nothing happens
    move_collision.on_collision(neighbor_move, 0)
    assert move_collision.sprite == "🥚"
    assert neighbor_move.sprite == "🥚"

    mock_collision = GameBlocks(["🥚"])  # so movable_positions is True
    collision_test = LevelCreateBlock(mock_collision)

    nomove_collision = collision_test._create_block("🥚", 0, 0, mock_collision)
    neighbor_nomove = collision_test._create_block("🧱", 0, -1, mock_collision)
    assert neighbor_nomove._type.name == BlockType.IMMOVABLE.name

    # nothing happens
    nomove_collision.on_collision(neighbor_nomove, 0)
    assert nomove_collision.sprite == "🥚"
    assert neighbor_nomove.sprite == "🧱"

    # EDGE CASE: Block passed is not Movable, raise AssertionError
    mock_collision = GameBlocks(["🥚"])  # so movable_positions is True
    collision_test = LevelCreateBlock(mock_collision)

    x_collision = collision_test._create_block("🧱", 0, 0, mock_collision)
    neighbor_x = collision_test._create_block("🟩", 0, 1, mock_collision)
    assert neighbor_x._type.name == BlockType.FLOOR.name

    x_collision.new_row = x_collision.row + neighbor_x.row
    x_collision.new_col = x_collision.col + neighbor_x.col
    with pytest.raises(AssertionError):
        x_collision.on_collision(neighbor_x, 0)

    # EDGE CASE: Neighbor doesn't exist
    mock_collision = GameBlocks(["🥚"])  # so movable_positions is True
    collision_test = LevelCreateBlock(mock_collision)

    y_collision = collision_test._create_block("🧱", 0, 0, mock_collision)
    with pytest.raises(NameError):
        y_collision.on_collision(neighbor_y, 0)

    # EDGE CASE: Block doesn't exist but neighbor does
    mock_collision = GameBlocks(["🥚"])  # so movable_positions is True
    collision_test = LevelCreateBlock(mock_collision)

    neighbor_z = collision_test._create_block("🪹", -1, 0, mock_collision)
    with pytest.raises(NameError):
        z_collision.on_collision(neighbor_z, 0)
    

    

def test_create_block() -> None:
    # Tests if Block object is Initialized Properly
    mock_create = GameCreateBlock()
    create_block_test = LevelCreateBlock(mock_create)

    # Normal Blocks, BlockType.name comparison
    block_egg = create_block_test._create_block("🥚", 0, 0, mock_create)
    assert block_egg._type.name == BlockType.MOVABLE.name
    assert block_egg.name == "Egg"
    assert block_egg.sprite == "🥚"

    block_grass = create_block_test._create_block("🟩", 0, 0, mock_create)
    assert block_grass._type.name == BlockType.FLOOR.name
    assert block_grass.name == "Grass"
    assert block_grass.sprite == "🟩"

    block_wall = create_block_test._create_block("🧱", 0, 0, mock_create)
    assert block_wall._type.name == BlockType.IMMOVABLE.name
    assert block_wall.name == "Wall"
    assert block_wall.sprite == "🧱"

    block_nest = create_block_test._create_block("🪹", 0, 0, mock_create)
    assert block_nest._type.name == BlockType.GOAL.name
    assert block_nest.name == "Nest"
    assert block_nest.sprite == "🪹"

    block_full = create_block_test._create_block("🪺", 0, 0, mock_create)
    assert block_full._type.name == BlockType.IMMOVABLE.name
    assert block_full.name == "Full Nest"
    assert block_full.sprite == "🪺"

    block_pan = create_block_test._create_block("🍳", 0, 0, mock_create)
    assert block_pan._type.name == BlockType.VOID.name
    assert block_pan.name == "Pan"
    assert block_pan.sprite == "🍳"

    block_hole = create_block_test._create_block(" ", 0, 0, mock_create)
    assert block_hole._type.name == BlockType.VOID.name
    assert block_hole.name == "Hole"
    assert block_hole.sprite == " "

    # Wrong Assertions
    block_egg = create_block_test._create_block("🥚", 0, 0, mock_create)
    assert not block_egg._type.name == BlockType.IMMOVABLE.name
    assert not block_egg.name == "Pan"
    assert not block_egg.sprite == "🟩"


    # EDGE CASE: self.game is undefined
    with pytest.raises(NameError):
        assert create_block_test._create_block("🥚", 0, 0, nonexistent_game)
        assert create_block_test._create_block("🥚", 0, 0, what_is_life)
        assert create_block_test._create_block("🥚", 0, 0, rain)


    # EDGE CASE: sprite is not passed or unrecognized
    with pytest.raises(KeyError):
        assert create_block_test._create_block("", 0, 0, mock_create)
        assert create_block_test._create_block("A", 0, 0, mock_create)
        assert create_block_test._create_block((0, 1), 0, 0, mock_create)
        assert create_block_test._create_block(12, 0, 0, mock_create)


def test_change_block_to() -> None:
    # Given a Sprite, Tests if Block is Changed Correctly
    mock_change = GameCreateBlock()
    mock_create_block = LevelCreateBlock(mock_change)

    # Normal Case (any block can work as long as it is defined)

    block_test = mock_create_block._create_block("🥚", 0, 0, mock_change)

    block_test._change_block_to(Sprite.GRASS)
    assert block_test.sprite == "🟩"
    assert block_test.name == "Grass"
    assert block_test._type.name == BlockType.FLOOR.name

    block_test._change_block_to(Sprite.WALL)
    assert block_test.sprite == "🧱"
    assert block_test.name == "Wall"
    assert block_test._type.name == BlockType.IMMOVABLE.name

    block_test._change_block_to(Sprite.NEST)
    assert block_test.sprite == "🪹"
    assert block_test.name == "Nest"
    assert block_test._type.name == BlockType.GOAL.name

    block_test._change_block_to(Sprite.FULL_NEST)
    assert block_test.sprite == "🪺"
    assert block_test.name == "Full Nest"
    assert block_test._type.name == BlockType.IMMOVABLE.name

    block_test._change_block_to(Sprite.PAN)
    assert block_test.sprite == "🍳"
    assert block_test.name == "Pan"
    assert block_test._type.name == BlockType.VOID.name

    block_test._change_block_to(Sprite.HOLE)
    assert block_test.sprite == " "
    assert block_test.name == "Hole"
    assert block_test._type.name == BlockType.VOID.name

    block_test._change_block_to(Sprite.EGG)
    assert block_test.sprite == "🥚"
    assert block_test.name == "Egg"
    assert block_test._type.name == BlockType.MOVABLE.name

    # EDGE CASE: Unrecognized Sprite Passed, raise AttributeError

    block_x = mock_create_block._create_block("🥚", 0, 0, mock_change)

    with pytest.raises(AttributeError):
        assert block_x._change_block_to(Sprite.NULL)
        assert block_x._change_block_to(Sprite.BRUH)
        assert block_x._change_block_to(Sprite.FLAG)
        assert block_x._change_block_to(Sprite.UGANDA)
        assert block_x._change_block_to(Sprite.KNUCKLES)


def test_delete() -> None:
    # Tests if Block is Converted to a FLOOR Block
    mock_delete = GameCreateBlock()
    delete_block_test = LevelCreateBlock(mock_delete)

    # Normal Cases, even if unusual besides Egg
    delete_egg = delete_block_test._create_block("🥚", 0, 0, mock_delete)
    delete_wall = delete_block_test._create_block("🧱", 0, 0, mock_delete)
    delete_grass = delete_block_test._create_block("🟩", 0, 0, mock_delete)
    delete_nest = delete_block_test._create_block("🪹", 0, 0, mock_delete)
    delete_full = delete_block_test._create_block("🪺", 0, 0, mock_delete)
    delete_pan = delete_block_test._create_block("🍳", 0, 0, mock_delete)
    delete_hole = delete_block_test._create_block(" ", 0, 0, mock_delete)

    delete_egg._delete()
    assert delete_egg.sprite == "🟩"
    assert delete_egg.name == "Grass"
    assert delete_egg._type.name == "FLOOR"
    assert mock_delete.score == -5

    mock_delete.score = 0  # Reset Score

    delete_wall._delete()
    assert delete_wall.sprite == "🟩"
    assert delete_wall.name == "Grass"
    assert delete_wall._type.name == "FLOOR"
    assert mock_delete.score == -5

    mock_delete.score = 0  # Reset Score

    delete_grass._delete()
    assert delete_grass.sprite == "🟩"
    assert delete_grass.name == "Grass"
    assert delete_grass._type.name == "FLOOR"
    assert mock_delete.score == -5

    mock_delete.score = 0  # Reset Score

    delete_nest._delete()
    assert delete_nest.sprite == "🟩"
    assert delete_nest.name == "Grass"
    assert delete_nest._type.name == "FLOOR"
    assert mock_delete.score == -5

    mock_delete.score = 0  # Reset Score

    delete_full._delete()
    assert delete_full.sprite == "🟩"
    assert delete_full.name == "Grass"
    assert delete_full._type.name == "FLOOR"
    assert mock_delete.score == -5

    mock_delete.score = 0  # Reset Score

    delete_pan._delete()
    assert delete_pan.sprite == "🟩"
    assert delete_pan.name == "Grass"
    assert delete_pan._type.name == "FLOOR"
    assert mock_delete.score == -5

    mock_delete.score = 0  # Reset Score

    delete_hole._delete()
    assert delete_hole.sprite == "🟩"
    assert delete_hole.name == "Grass"
    assert delete_hole._type.name == "FLOOR"
    assert mock_delete.score == -5

    mock_delete.score = 0  # Reset Score


    # EDGE CASE: Block does not exist in the first place

    with pytest.raises(NameError):
        assert delete_null._delete()
        assert delete_what._delete()
        assert delete_itworks._delete()
