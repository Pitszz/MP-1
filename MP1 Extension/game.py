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
    def __init__(self, filename: str):
        self.level_data = Level(self, filename)
        self.display_manager = DisplayManager(self)

        self.score: int = 0
        self.grid: list[list[Block]] = self.level_data.grid
        self.moves: int = self.level_data.max_moves
        self.current_move: str = ""
        self.previous_moves: list[str] = []

    def play(self):
        while not self.is_end_state():
            self.display_manager.display()

            player_input = self.get_input(
                input("Enter direction: "), set(DIRECTION_MAP.keys())
                )

            for move in self.get_moves_to_process(player_input, self.moves):
                if move == "Q":
                    break
                elif move in DIRECTION_MAP:
                    self.current_move = DIRECTION_MAP[move]
                    self.previous_moves.append(move)
                    self.moves -= 1
                    self.process_move(self.current_move)
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
        """Returns the corresponding iteration order of the rows and
        cols given a direction.
        """
        match increment:
            case Direction.FORWARD | Direction.LEFT:
                return range(len(self.level_data.movables_positions))
            case Direction.BACKWARD | Direction.RIGHT:
                return range(
                    len(self.level_data.movables_positions) - 1, -1, -1
                    )

    def is_end_state(self) -> bool:
        return self.moves <= 0 or self.no_movables_left()

    def is_inside(self, new_row: int, rows: int, new_col: int,
                  cols: int) -> bool:
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbor: Block = self.grid[new_row][new_col]

        return self.match_neighbor(neighbor)

    def match_neighbor(self, neighbor) -> bool:
        match neighbor._type:
            case BlockType.FLOOR | BlockType.VOID | BlockType.GOAL:
                return True
            case _:
                return False

    def all_objects_blocked(self, rows, cols, direction: Direction) -> bool:
        for x in self.get_range(direction):
            i, j = self.level_data.movables_positions[x]
            block = self.grid[i][j]
            assert block._type == BlockType.MOVABLE
            (new_row, new_col) = direction.value
            new_row += i
            new_col += j
            if self.is_inside(new_row, rows, new_col, cols):
                return False
            else:
                continue

        return True

    def no_movables_left(self) -> bool:
        for row in self.grid:
            for block in row:
                if block._type == BlockType.MOVABLE:
                    return False

        return True


class DisplayManager:
    def __init__(self, game: Game):
        self.game = game

    def display(self):
        self.display_level()
        self.display_status()

    def display_level(self):
        self.clear_screen()
        grid = self.game.grid
        print()

        for row in grid:
            print("".join(block.sprite for block in row))

    def display_status(self) -> None:
        print(f"Score: {self.game.score}")
        print(f"Moves: {self.game.moves}/{self.game.level_data.max_moves}")
        print(f"Previous Moves: {self.convert_moves_to_arrows(
            self.game.previous_moves
            )}")

    def clear_screen(self) -> None:
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
    def __init__(self, name: str, sprite: str, _type: BlockType, row: int,
                 col: int, game: Game):
        self.game = game
        self.name = name
        self.sprite = sprite
        self._type = _type
        self.row = row
        self.col = col

    def move(self, direction: Direction, x: int):
        (row, col) = direction.value
        self.new_row = self.row + row
        self.new_col = self.col + col

        if (0 <= self.new_row < self.game.level_data.rows and
                0 <= self.new_col < self.game.level_data.cols):
            self.on_collision(self.game.grid[self.new_row][self.new_col], x)

    def on_collision(self, neighbor: Self, x: int):
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

    def _delete(self):
        self._change_block_to(Sprite.GRASS)
        self.game.score += Config.SUBSTRACT_SCORE

    def _change_block_to(self, sprite: str):
        (name, block_type) = BLOCK_MAP[sprite]

        # print(f"Changing {repr(self.name)} block to", name)

        self.sprite = sprite
        self.name = name
        self._type = block_type


class Level:
    def __init__(self, game: Game, filename: str, folder: str = "levels"):
        self.grid: list[list[Block]] = []
        self.rows: int = 0
        self.cols: int = 0
        self.max_moves: int = 0

        self.game: Game = game
        self.movables_positions: list[tuple] = []
        self._load_level(filename, folder)

    def _load_level(self, filename: str, folder: str) -> None:
        file_path = os.path.join(folder, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.rows = int(file.readline())
                self.max_moves = int(file.readline())

                for row in range(self.rows):
                    line = file.readline().strip()
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
