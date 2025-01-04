import os
import sys
import time
import subprocess

from utils import (
    GameState,
    Direction,
    BlockType,
    Sprite,
    Config,
    BLOCK_MAP,
    DIRECTION_MAP,
    ARROW_MAP
    )

from typing import Self, Iterable, Generator


class Game:
    """This is the Game class. When a valid filename is given, it will
    initialize a level based on the data found in the specific stage
    file like the rows, maximum amount of moves and the puzzle grid.
    The main game loop and input handling are encapsulated inside as
    class methods.
    """
    def __init__(self, filename: str):
        # Takes in a filename, initializes the Game object
        self.level_data = Level(self, filename)
        self.display_manager = DisplayManager(self)

        self.score: int = 0
        self.grid: list[list[Block]] = self.level_data.grid
        self.moves: int = self.level_data.max_moves
        self.current_move: str = ""
        self.previous_moves: list[str] = []

    def play(self) -> None:
        """Encompasses the main game loop."""
        while not self.is_end_state():
            self.display_manager.display()

            player_input = self.get_input(
                input("Enter direction: "), set('lfrbQ')
                )

            if player_input == "Q":
                break

            for move in self.get_moves_to_process(player_input, self.moves):
                if move in DIRECTION_MAP:
                    self.move_dir: Direction = DIRECTION_MAP[move]
                    self.previous_moves.append(move)
                    self.moves -= 1
                    self.process_move(self.move_dir)
                else:
                    print("Invalid Move")

    def get_input(self, prompt: str, valid_inputs: set[str]) -> list[str]:
        """Returns the valid inputs of the player as a list."""
        player_input: str = prompt.strip().lower()

        moves: list[str] = []

        for char in player_input:
            if self.is_valid_input(char, valid_inputs):
                moves.append(char)

        return moves

    def is_valid_input(self, player_input: str, valid_inputs: set) -> bool:
        """Checks whether a given input is valid."""
        return player_input in valid_inputs

    def get_moves_to_process(self, moves: Iterable,
                             moves_left: int) -> Generator:
        """Yields the moves to be processed given the remaining moves."""
        moves = iter(moves)

        for _ in range(moves_left):
            try:
                yield next(moves)
            except StopIteration:
                break

    def process_move(self, direction: Direction):
        """Given a direction, move the movable objects onto that
        direction until all are blocked. Update the display for each
        movement done.
        """
        rows = self.level_data.rows
        cols = self.level_data.cols

        while not self.all_objects_blocked(rows, cols, direction):
            self.remove_movables: list[int] = []

            for x in self.get_range(direction):
                i, j = self.level_data.movables_positions[x]
                block = self.grid[i][j]
                assert block._type == BlockType.MOVABLE
                block.move(direction, x)

            for e in reversed(self.remove_movables):
                # iterating in reverse to avoid IndexErrors
                self.level_data.movables_positions.pop(e)

            self.display_manager.display()
            time.sleep(Config.MOVE_DELAY)

    def get_range(self, increment: Direction) -> range:
        """Returns the corresponding iteration order of every movable
        object still in the grid given a direction.
        """
        match increment:
            case Direction.FORWARD | Direction.LEFT:
                return range(len(self.level_data.movables_positions))
            case Direction.BACKWARD | Direction.RIGHT:
                return range(
                    len(self.level_data.movables_positions) - 1, -1, -1
                    )

    def is_end_state(self) -> bool:
        """End state detection if there are no moves left or if there are
        no more movables in the grid.
        """
        return self.moves <= 0 or self.no_movables_left()

    def is_inside(self, new_row: int, new_col: int, rows: int,
                  cols: int) -> bool:
        """Checks if the neighboring block to the movable is inside
        the grid or not before checking if the neighbor can be moved
        onto.
        """
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbor: Block = self.grid[new_row][new_col]
            return self.is_movable_to(neighbor)
        else:
            return False

    def is_movable_to(self, neighbor) -> bool:
        """Checks if neighboring block can be moved onto."""
        match neighbor._type:
            case BlockType.FLOOR | BlockType.VOID | BlockType.GOAL:
                return True
            case _:
                return False

    def all_objects_blocked(self, rows, cols, direction: Direction) -> bool:
        """Checks if every movable in the grid can move or not. If
        True, the turn continues. If False, the turn ends and a new
        move is processed.
        """
        for x in self.get_range(direction):
            i, j = self.level_data.movables_positions[x]
            block = self.grid[i][j]
            assert block._type == BlockType.MOVABLE
            (new_row, new_col) = direction.value
            new_row += i
            new_col += j
            if self.is_inside(new_row, new_col, rows, cols):
                return False
            else:
                continue

        return True

    def no_movables_left(self) -> bool:
        """Checks if there are still movable objects in the grid."""
        for row in self.grid:
            for block in row:
                if block._type == BlockType.MOVABLE:
                    return False

        return True


class DisplayManager:
    """Creates a DisplayManager instance that is passed to the Game
    object. Main function is showing the player the game state by
    printing the grid and specific level data in the terminal.
    """
    def __init__(self, game: Game):
        self.game = game

    def display(self):
        """Parent function to the level and status displays."""
        self.display_level()
        self.display_status()

    def display_level(self):
        """Prints the grid as rows of strings."""
        self.clear_screen()
        grid = self.game.grid
        print()

        for row in grid:
            print("".join(block.sprite for block in row))

    def display_status(self) -> None:
        """Displays the player's current score and moves."""
        print(f"Score: {self.game.score}")
        print(f"Moves: {self.game.moves}/{self.game.level_data.max_moves}")
        print(f"Previous Moves: {self.convert_moves_to_arrows(
            self.game.previous_moves
            )}")

    def clear_screen(self) -> None:
        """Clears the previous screen in terminal."""
        if sys.stdout.isatty():
            clear_cmd = "cls" if os.name == "nt" else "clear"
            subprocess.run([clear_cmd], shell=True)

    def convert_moves_to_arrows(self, previous_moves: list[str],
                                max_length: int = 20) -> str:
        converted = "".join([ARROW_MAP[move]
                            for move in previous_moves[-max_length:]])

        if len(previous_moves) > max_length:
            return "..." + converted
        else:
            return converted


class Block:
    """Initializes a Block object that has attributes that can be
    modified as the game progresses. An instance is created by a Level
    which in turn is initialized by a Game object.
    """
    def __init__(self, name: str, sprite: str, _type: BlockType, row: int,
                 col: int, game: Game):
        self.game = game
        self.name = name
        self.sprite = sprite
        self._type = _type
        self.row = row
        self.col = col

    def move(self, direction: Direction, x: int) -> None:
        """Given a direction and index value, move the Movable to a
        new position based on the direction.
        """
        (row, col) = direction.value
        self.new_row = self.row + row
        self.new_col = self.col + col

        if (0 <= self.new_row < self.game.level_data.rows and
                0 <= self.new_col < self.game.level_data.cols):
            self.on_collision(self.game.grid[self.new_row][self.new_col], x)

    def on_collision(self, neighbor: Self, x: int) -> None:
        """Checks the neighbor of the Movable and determines what to
        do depending on the BlockType.
        """
        assert self._type == BlockType.MOVABLE
        # print("Yes i am egg")
        # print("Neighbor type is", neighbor._type)
        match neighbor._type:
            case BlockType.FLOOR:
                neighbor._change_block_to(Sprite.EGG)
                self._change_block_to(Sprite.GRASS)
                self.game.level_data.movables_positions[x] = (
                    self.new_row, self.new_col
                    )
            case BlockType.VOID:
                self._delete()
                self.game.remove_movables.append(x)
            case BlockType.GOAL:
                neighbor._change_block_to(Sprite.FULL_NEST)
                self._change_block_to(Sprite.GRASS)
                self.game.score += Config.ADD_SCORE + self.game.moves + 1
                self.game.remove_movables.append(x)

    def _delete(self) -> None:
        """Converts Block to Grass and subtracts score."""
        self._change_block_to(Sprite.GRASS)
        self.game.score += Config.SUBSTRACT_SCORE

    def _change_block_to(self, sprite: str) -> None:
        """Changes current Block to the passed block character."""
        (name, block_type) = BLOCK_MAP[sprite]

        # print(f"Changing {repr(self.name)} block to", name)

        self.sprite = sprite
        self.name = name
        self._type = block_type


class Level:
    """Gathers the data stored in a specific file. The Level object
    also creates a new grid filled with Block objects based on
    information from the sprite in connection with util.py.
    """
    def __init__(self, game: Game, filename: str, folder: str = "levels"):
        self.grid: list[list[Block]] = []
        self.rows: int = 0
        self.cols: int = 0
        self.max_moves: int = 0

        self.game: Game = game
        self.movables_positions: list[tuple] = []
        self._load_level(filename, folder)

    def _load_level(self, filename: str, folder: str) -> None:
        """Given a filename, reads the stage data inside the file and
        generates a grid with Block objects.
        """
        file_path = os.path.join(folder, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.rows = int(file.readline())
                self.max_moves = int(file.readline())

                for row in range(self.rows):
                    line = file.readline().strip('\n')
                    grid_row = [
                        self._create_block(char, row, col, self.game)
                        for (col, char) in enumerate(line)
                    ]
                    self.grid.append(grid_row)

                self.cols = len(self.grid[0])

        except FileNotFoundError:
            print(f"File {filename} not found")
            sys.exit()

    def _create_block(
            self, char: str, row: int, col: int, game: Game) -> Block:
        """Creates a Block object that has a given set of attributes
        based on the name, Sprite, BlockType andposition in the grid.
        """
        (name, block_type) = BLOCK_MAP[char]
        if block_type == BlockType.MOVABLE:
            self.movables_positions.append((row, col))

        return Block(name, char, block_type, row, col, self.game)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("The game requires a level file to run.")
        sys.exit()

    filename = sys.argv[1]
    game = Game(filename)
    game.play()
