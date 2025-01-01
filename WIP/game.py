import os
import sys
import subprocess

from time import sleep
from enum import Enum, auto
from dataclasses import dataclass
from collections.abc import Iterable, Generator


class Blocks(Enum):
    EGG = "🥚"
    WALL = "🧱"
    GRASS = "🟩"
    NEST = "🪹"
    FULL_NEST = "🪺"
    PAN = "🍳"
    VOID = " "


class Dir(Enum):
    FORWARD = (-1, 0)
    LEFT = (0, -1)
    BACKWARD = (1, 0)
    RIGHT = (0, 1)


@dataclass
class LevelData:
    rows: int
    cols: int
    max_moves: int
    moves_left: int
    points: list[int]
    previous_moves: list[str]
    current_move: str
    puzzle: list[list[str]]


class Game:
    """
    Encompasses the main game loop. The functions that deal with
    user input and end_state detection are encapsulated here.
    """
    def __init__(self) -> None:
        # Initializes the level specifics
        self.level: LoadLevel = LoadLevel(sys.argv)
        self.controls: set[str] = set("lfrb")
        self.display: Display = Display(self.level.level_data)
        self.egg_moves: Egg = Egg(self.level.level_data, self.display)

        self.main_loop()

    def main_loop(self) -> None:
        self.level_data = self.level.level_data

        def prompt_player(get_input) -> list[str]:
            return get_input(
                input("Enter your move(s): "), self.controls
                )

        def process_all_moves() -> None:
            for move in self.valid_moves:
                self.level_data.current_move = move
                self.level_data.previous_moves.append(move)
                self.egg_moves.process_move(move, self.level_data)
                self.level_data.moves_left -= 1

        while not self.is_end_state(self.level_data):
            # Update the display every frame
            self.display.update_display()

            moves_left: int = self.level_data.moves_left
            previous_moves: list[str] = self.level_data.previous_moves
            player_input: list[str] = prompt_player(self.get_input)
            # pass get_input to player_input since latter
            # is an inner function unable to access the former

            # Prompts the user again if there is no valid input
            if not player_input:
                print("No valid moves")
                sleep(0.5)
                continue

            # Collects all the valid moves within limited moves
            self.valid_moves: list[str] = [*self.get_moves_to_process(
                player_input, moves_left, previous_moves
                )
            ]

            # Goes through all the moves
            process_all_moves()

        self.game_over()

    # Input Handling
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

    def get_moves_to_process(self, moves: Iterable, moves_left: int,
                             previous_moves: list[str]) -> Generator:
        """Yields the moves to be processed given the remaining moves."""
        moves = iter(moves)

        for _ in range(moves_left):
            try:
                yield next(moves)
            except StopIteration:
                break

    def is_end_state(self, level_data: LevelData) -> bool:
        """Returns true if there are no more eggs left or you have no
        more moves left.
        """
        moves_left: int = level_data.moves_left
        grid: list[list[str]] = level_data.puzzle

        return moves_left <= 0 or self.no_eggs_left(grid)

    def no_eggs_left(self, grid: list[list[str]]) -> bool:
        """Checks whether there are still eggs in the grid."""
        for row in grid:
            set_row: set = set(row)

            if Blocks.EGG.value in set_row:
                return False

        return True

    def game_over(self) -> None:
        """Displays the final state of the grid and summary of the
        game.
        """
        clear_screen()
        self.display.update_display(True)
        sys.exit()


class Display:
    """
    Display functions are separated from the main game logic and user inputs.
    """
    def __init__(self, level_data: LevelData):
        self.level_data: LevelData = level_data

    def update_display(self, end_state: bool = False) -> None:
        """Displays the current state of the grid along with the stats."""
        self.puzzle: list[list[str]] = self.level_data.puzzle
        clear_screen()
        self.display_puzzle()
        self.display_stats(end_state)

    def display_puzzle(self) -> None:
        """Prints the current state of the puzzle."""
        for row in self.level_data.puzzle:
            print("".join(row))

    def display_stats(self, end_state: bool) -> None:
        """Prints the stats of the level."""
        points: int = sum(self.level_data.points)
        max_moves: int = self.level_data.max_moves
        moves_left: int = self.level_data.moves_left
        previous_moves: str = self.convert_to_arrows(
            self.level_data.previous_moves
            )

        if end_state:
            message: str = f"""Congratulations! You got a total of {points}
             points!"""
            if points < 0:
                message = f"""Just keep on trying! You can turn that {points}
                 points to positive!"""

            print(message.replace('\n', '').replace('  ', ''))
            # the second replace removes the tabs
            print(f"Total moves done: {max_moves - moves_left}/{max_moves}")
            print(f"Moves played: {previous_moves}")

        else:
            print(f"Points: {points}")
            print(f"Remaining moves: {moves_left}/{max_moves}")
            print(f"Previous moves: {previous_moves}")

    def convert_to_arrows(
            self, previous_moves: list[str] | str,
            max_length: int = 20) -> str:
        """Returns a string of converted moves to their respective
        arrow equivalent. Max length of arrows shown is completely
        arbitrary
        """
        conversion: dict = {
            "l": "←",
            "r": "→",
            "f": "↑",
            "b": "↓",
        }

        # Replaces the string with '...←↑↓' in case it's too long
        converted: str = "".join(
            [conversion[move] for move in previous_moves[-max_length:]]
            )

        if len(previous_moves) > max_length:
            return "..." + converted
        else:
            return converted


class Egg:
    """Movement Processes go here."""
    def __init__(self, level_data: LevelData, display: Display):
        # initialize a list of where the eggs are
        self.egg_coordinates: list[tuple] = []
        self.display: Display = display

        self.get_eggs_pos(level_data.puzzle)

    def get_eggs_pos(self, grid: list[list[str]]) -> list[tuple]:
        """Returns all the positions of the eggs at the start."""
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                match grid[r][c]:
                    case Blocks.EGG.value:
                        self.egg_coordinates.append((r, c))
                    case _:
                        continue

        return self.egg_coordinates

    def process_move(self, move: str, level_data: LevelData) -> None:
        """Continuously moves the eggs until all eggs are blocked."""
        # Maps the move to its respective direction increments
        increments: dict = {
            "f": Dir.FORWARD,
            "b": Dir.BACKWARD,
            "l": Dir.LEFT,
            "r": Dir.RIGHT
            }

        direction = increments[move]

        puzzle: list[list[str]] = level_data.puzzle
        rows, cols = level_data.rows, level_data.cols

        # Update display and move until the eggs cannot move further
        while not self.all_eggs_blocked(level_data, direction):
            clear_screen()
            puzzle = self.move_eggs(puzzle, direction, rows, cols, level_data)
            level_data.puzzle = puzzle

            self.display.display_puzzle()
            current_move = level_data.current_move
            currently_moving = self.display.convert_to_arrows(current_move)
            print(f"Currently moving: {currently_moving}")
            sleep(0.35)

    def move_eggs(self, grid: list[list[str]], direction: Dir, rows: int,
                  cols: int, level_data: LevelData) -> list[list[str]]:
        """Handles the movement of the eggs dynamically for all
        direction by returning a new grid with updated positions.

        It also updates the scores accordingly.
        """
        (di, dj) = direction.value
        removed_eggs: list[int] = []
        new_grid: list[list[str]] = [row[:] for row in grid]

        def matching_type(new_grid: list[list[str]],
                          old_coords: tuple[int, int],
                          neighbor_idx: tuple[int, int], rows: int,
                          cols: int, x: int) -> None:
            ni, nj = neighbor_idx
            i, j = old_coords
            # Neighbor would be current pos of egg + increment
            if self.is_inside(ni, nj, rows, cols):
                neighbor = new_grid[ni][nj]
                match neighbor:
                    case Blocks.GRASS.value:
                        new_grid[i][j] = Blocks.GRASS.value
                        new_grid[ni][nj] = Blocks.EGG.value
                        self.egg_coordinates[x] = (ni, nj)
                    case Blocks.NEST.value:
                        new_grid[i][j] = Blocks.GRASS.value
                        new_grid[ni][nj] = Blocks.FULL_NEST.value
                        removed_eggs.append(x)
                        level_data.points.append(
                            10 + level_data.moves_left
                            )
                    case Blocks.PAN.value | Blocks.VOID.value:
                        new_grid[i][j] = Blocks.GRASS.value
                        removed_eggs.append(x)
                        level_data.points.append(-5)

        # Iterate through the grid, searching for the eggs
        # instead of this, iterate through the egg_coords &
        for x in self.get_range(direction):
            i, j = self.egg_coordinates[x]
            ni, nj = i + di, j + dj
            matching_type(new_grid, (i, j), (ni, nj), rows, cols, x)

        for e in reversed(removed_eggs):
            # iterating in reverse to avoid IndexErrors
            self.egg_coordinates.pop(e)

        return new_grid

    def all_eggs_blocked(self, level_data: LevelData, d: Dir) -> bool:
        """Returns True if all of the eggs cannot be moved further."""
        puzzle = level_data.puzzle
        rows, cols = level_data.rows, level_data.cols
        eggs_pos = self.egg_coordinates

        (di, dj) = d.value
        for i, j in eggs_pos:
            # Checks the neighbor given an increment
            ni, nj = i + di, j + dj
            if self.is_inside(ni, nj, rows, cols):
                neighbor = puzzle[ni][nj]
                # We can move the egg still if the neighbor is grass,
                # pan or empty nest
                match neighbor:
                    case (Blocks.GRASS.value |
                          Blocks.PAN.value | Blocks.NEST.value):
                        return False
                    case _:
                        continue

        return True

    def is_inside(self, i: int, j: int, rows: int, cols: int) -> bool:
        """Checks whether the neighbor is inside the grid."""
        return 0 <= i < rows and 0 <= j < cols

    def get_range(self, increment: Dir) -> range:
        """Returns the corresponding iteration order of the rows and
        cols given a direction.
        """
        match increment:
            case Dir.FORWARD | Dir.LEFT:
                return range(len(self.egg_coordinates))
            case Dir.BACKWARD | Dir.RIGHT:
                return range(len(self.egg_coordinates) - 1, -1, -1)


class LoadLevel:
    def __init__(self, filename: list[str]) -> None:
        """Initializes the level. This checks if a
        valid filename was given, otherwise the program exits.
        """
        self.filename = filename

        if len(filename) < 2:
            print("The game requires a filename to start.", file=sys.stderr)
            sys.exit()
        else:
            self.file_path = os.path.join("levels", self.filename[1])

        self.load_level()

    def load_level(self):
        """Creates a LevelData object with information regarding the
        level, including the puzzle grid. The program exits if the
        filename is not in the levels folder. To ensure that LevelData
        will be filled up correctly, variables containing the necessary
        information are declared first before passing to LevelData.
        """
        try:

            with open(self.file_path, encoding="utf-8") as file:
                rows = int(file.readline())
                max_moves = int(file.readline())
                moves_left = max_moves
                puzzle = [
                    list(file.readline().strip("\n"))
                    for _ in range(rows)
                ]
                cols = len(puzzle[0])

        except FileNotFoundError:
            sys.exit(f"""{self.filename[1]} does not exist in the specified
             'levels' folders.""".replace('\n', '').replace('  ', ''))

        points = [0]
        previous_moves = []
        current_move = ""

        self.level_data = LevelData(rows, cols, max_moves, moves_left, points,
                                    previous_moves, current_move, puzzle)

        print("Welcome to Egg Roll!")
        sleep(0.5)


# Helper Function
def clear_screen() -> None:
    """Clears the terminal screen, if any"""
    if sys.stdout.isatty():
        clear_cmd = "cls" if os.name == "nt" else "clear"
        subprocess.run([clear_cmd], shell=True)


if __name__ == '__main__':
    main = Game()
