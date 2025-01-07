import sys
import time

from managers import DisplayManager, InputManager, ScoreManager
from utils import (
    Direction,
    GameState,
    BlockType,
    Path,
    Config,
    INPUT_TO_DIRECTION
    )
from block import Block
from level import Level
from leaderboard import Leaderboard


class Game:
    """Represents the main game object.

    It handles the different game states and makes use
    of compositions to manage most of the game properties.
    """

    def __init__(self) -> None:
        # Game Components
        self.level = Level()
        self.display_manager = DisplayManager()
        self.input_manager = InputManager()
        self.score_manager = ScoreManager()
        self.leaderboard = Leaderboard()

        # Game Attributes
        self.state: GameState = GameState.PLAYING
        self.grid: list[list[Block]] = [[]]
        self.moves_left: int = 0
        self.current_move: str = ""
        self.previous_moves: list[str] = []
        self.movables_positions: list[tuple] = []

    # Gameplay State

    def play(self) -> None:
        """Main game loop that handles the different game states."""
        self.initialize_game()

        # Initializes the necessary files for the leaderboards to work
        filename: str = sys.argv[1]
        level_name: str = self.level.get_level_name(filename)
        self.leaderboard.initialize_leaderboard(
            level_name, Path.LEADERBOARDS_FOLDER)

        # State Handling
        while True:
            if self.state == GameState.PLAYING:
                self.handle_gameplay()
            elif self.state == GameState.GAME_OVER:
                self.handle_game_over(level_name)
            elif self.state == GameState.LEADERBOARDS:
                self.handle_leaderboards(level_name)

    def initialize_game(self) -> None:
        """Checks if a level file was given, if yes it initializes the
        value of game attributes, otherwise exit the program.
        """
        if len(sys.argv) < 2:
            print("The game requires a level file to start.\n")
            sys.exit()

        filename: str = sys.argv[1]
        self.level.load_level(filename, Path.LEVELS_FOLDER)

        self.grid = self.level.get_initial_grid()
        self.moves_left = self.level.get_max_moves()
        self.movables_positions = self.level.get_movables_positions(
        )

    def handle_gameplay(self) -> None:
        """Handles the main gameplay logic."""
        rows: int = self.level.rows
        cols: int = self.level.cols

        while not self.is_end_state(self.moves_left, self.grid):
            # Display the current state of grid
            self.display_manager.update(
                self.grid, self.score_manager.get_score(), self.moves_left,
                self.level.get_max_moves(), self.previous_moves
                )

            _input: str = input(Config.PROMPT).lower().strip()

            # Check if user enters a command
            if _input in Config.EXIT_COMMANDS:
                sys.exit()
            elif _input in Config.LEADERBOARD_COMMANDS:
                self.state = GameState.LEADERBOARDS
                return

            # Otherwise, process the input
            player_input: list[str] = self.input_manager.get_input(
                _input, Config.VALID_INPUTS)

            # If there are no valid inputs, prompt the user again
            if not player_input:
                print("\n< Invalid Input >")
                time.sleep(Config.MOVE_DELAY)
                continue

            moves: list[str] = [*self.input_manager.get_moves_to_process(
                player_input, self.moves_left)]

            # Process all the moves
            for move in moves:
                self.process_move(move, rows, cols)
                self.moves_left -= 1
                self.previous_moves.append(move)

        # Once end state is detected, change state to GAME_OVER
        self.state = GameState.GAME_OVER

    def process_move(self, move: str, rows: int, cols: int) -> None:
        """Given a direction, move the movable objects onto that
        direction until all are blocked. Update the display for
        each movement done.
        """
        direction = INPUT_TO_DIRECTION[move]

        while not self.all_movables_blocked(rows, cols, direction):
            self.movables_index: list[int] = []

            for idx in self.get_range(direction):
                (i, j) = self.movables_positions[idx]
                block: Block = self.grid[i][j]
                assert block.type == BlockType.MOVABLE

                block.move(self, self.score_manager,
                           self.moves_left, direction, idx)

            for idx in reversed(self.movables_index):
                # iterating in reverse to avoid IndexErrors
                self.movables_positions.pop(idx)

            self.display_manager.move_grid(self.grid, move)

    def is_end_state(self, moves_left: int, grid: list[list[Block]]) -> bool:
        """Checks if the game has reached an end state."""
        return moves_left <= 0 or self.no_movables_left(grid)

    def no_movables_left(self, grid: list[list[Block]]) -> bool:
        """Checks if there are no more movable blocks left."""
        for row in grid:
            for block in row:
                if block.type == BlockType.MOVABLE:
                    return False

        return True

    def all_movables_blocked(self, rows: int, cols: int,
                             direction: Direction) -> bool:
        """Checks if every movable in the grid can move or not. If
        True, the turn continues. If False, the turn ends and a new
        move is processed.
        """
        for idx in self.get_range(direction):
            row, col = self.movables_positions[idx]
            block = self.grid[row][col]
            assert block.type == BlockType.MOVABLE

            (i, j) = direction.value
            ni = row + i
            nj = col + j
            neighbor = self.grid[ni][nj]

            if (self.is_inside_grid(ni, nj, rows, cols) and
                    self.is_movable_to(neighbor)):
                return False

        return True

    def is_movable_to(self, neighbor: Block) -> bool:
        """Checks if neighboring block can be moved onto."""
        match neighbor.type:
            case BlockType.FLOOR | BlockType.VOID | BlockType.GOAL:
                return True
            case _:
                return False

    def is_inside_grid(self, i: int, j: int, rows: int, cols: int) -> bool:
        """Returns true if the given position is inside the grid."""
        return 0 <= i < rows and 0 <= j < cols

    def get_range(self, direction: Direction) -> range:
        """Returns the corresponding iteration order of every movable
        object still in the grid given a direction.
        """
        match direction:
            case Direction.FORWARD | Direction.LEFT:
                return range(len(self.movables_positions))
            case Direction.BACKWARD | Direction.RIGHT:
                return range(
                    len(self.movables_positions) - 1, -1, -1
                )

    # Other States

    def handle_game_over(self, filename: str) -> None:
        """Displays the final game state and exits the game."""
        self.display_manager.display_game_over(
            self.grid, self.score_manager.get_score(), self.moves_left,
            self.level.get_max_moves(), self.previous_moves
            )

        player_input = input(
            "\nAdd yourself to the leaderboard? (Y/N): ").strip().lower()

        if player_input in ("yes", "y"):
            pass
        elif player_input in ("no", "n"):
            sys.exit()
        else:
            print("\n< Invalid Input >")
            time.sleep(Config.MOVE_DELAY)
            return

        name = input("Enter name: ").strip()
        score = self.score_manager.get_score()
        moves = len(self.previous_moves)
        self.leaderboard.add_to_leaderboard(filename, name, score, moves)

        leaderboard = self.leaderboard.get_leaderboard(
            f"{filename}_leaderboard.json")
        self.display_manager.display_leaderboards(leaderboard)
        sys.exit()

    def handle_leaderboards(self, level_name: str) -> None:
        """Switches to the leaderboards state."""
        json_file = f"{level_name}_leaderboard.json"
        leaderboard = self.leaderboard.get_leaderboard(json_file)

        self.display_manager.display_leaderboards(leaderboard)
        self.state = GameState.PLAYING


if __name__ == "__main__":
    egg_roll = Game()
    egg_roll.play()
