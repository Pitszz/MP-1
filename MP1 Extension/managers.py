import os
import sys
import time
import subprocess

from typing import Iterable, Generator
from block import Block
from utils import Config, MOVE_TO_ARROW


class DisplayManager:
    """Represents the Display Component that is passed to the Game Class.

    It handles all UI related methods like displaying the grid, the
    player's current stats, leaderboards, etc.
    """

    def __init__(self) -> None:
        pass

    def update(self, grid: list[list[Block]], score: int, moves: int,
               max_moves: int, previous_moves: list[str]) -> None:
        """Displays the current state of the grid and the stats."""
        self.clear_screen()
        self.display_grid(grid)
        self.display_stats(score, moves, max_moves, previous_moves)

    def display_grid(self, grid: list[list[Block]]) -> None:
        """Prints the grid as a row of strings."""
        for row in grid:
            print("".join(block.sprite for block in row))

    def move_grid(self, grid: list[list[Block]], move: str) -> None:
        """Displays the grid and the direction it's currently moving
        towards.
        """
        self.clear_screen()
        self.display_grid(grid)
        print("Moving: " + MOVE_TO_ARROW[move])
        time.sleep(Config.MOVE_DELAY)

    def display_stats(self, score: int, moves: int, max_moves: int,
                      previous_moves: list[str]) -> None:
        """Displays the player's current score, moves left, and your
        previous moves.
        """
        print(f"Score: {score}")
        print(f"Moves: {moves}/{max_moves}")
        print(
            f"Previous Moves: {self.convert_moves_to_arrow(previous_moves)}"
            )

    def display_game_over(self, grid: list[list[Block]], score: int,
                          moves_left: int, max_moves: int,
                          previous_moves: list[str]) -> None:
        """Displays a summary of your game."""
        self.clear_screen()
        self.display_grid(grid)

        time.sleep(Config.MOVE_DELAY)
        message = (f"Congratulations! You got a total of {score} points")
        print(f"\n{message} in {max_moves - moves_left} moves!")
        print(
            f"Previous Moves: {self.convert_moves_to_arrow(
                previous_moves, 100
            )}"
        )

        time.sleep(1)

    def clear_screen(self) -> None:
        """Clears the screen, if any."""
        if sys.stdout.isatty():
            clear_cmd = "cls" if os.name == "nt" else "clear"
            subprocess.run([clear_cmd], shell=True)

    def convert_moves_to_arrow(self, previous_moves: list[str],
                               max_length: int = 20) -> str:
        """Converts the moves to their arrow equivalent, it also
        truncates it.
        """
        converted = "".join([MOVE_TO_ARROW[move]
                            for move in previous_moves[-max_length:]])

        if len(previous_moves) > max_length:
            return "..." + converted
        else:
            return converted

    def display_leaderboards(self, leaderboard: dict) -> None:
        """Displays the leaderboard for the level."""
        headers = ["RANK", "NAME", "POINTS", "MOVES"]
        sorted_scores = sorted(
            leaderboard["scores"], key=lambda x: (-x["score"],
                                                  x["moves"], x["name"])
        )

        rows = [
            [
                f"{rank:02}",
                entry["name"],
                str(entry["score"]),
                str(entry["moves"]),
            ]
            for rank, entry in enumerate(sorted_scores, 1)
        ]

        self.display_table(
            headers, rows, f'--- Leaderboard: {leaderboard["level"]} ---')
        input(f"\n→ Press [Enter] to continue.")

    def display_table(self, headers: list[str], rows: list[list[str]],
                      section_title: str = "Table"):
        """Displays a dynamic table with given headers, rows, and a
        section title.
        """
        self.clear_screen()

        # Adjust col widths based on the longest str in each col
        all_rows = [headers] + rows
        col_width = [max(len(row[col]) for row in all_rows)
                     for col in range(len(headers))]

        # Border styles
        TL, TR = "╭", "╮"
        BL, BR = "╰", "╯"
        HR, VR = "─", "│"
        MT, MB, ML, MR, MC = "┬", "┴", "├", "┤", "┼"

        # Horizontal borders
        top_border = TL + MT.join(
            HR * (width + 2) for width in col_width
            ) + TR
        bottom_border = BL + MB.join(
            HR * (width + 2) for width in col_width
            ) + BR
        separator = ML + MC.join(
            HR * (width + 2) for width in col_width
            ) + MR

        # Header row
        header_row = (
            VR
            + VR.join(
                f" {headers[i].center(col_width[i])} "
                for i in range(len(headers))
            )
            + VR
        )

        # Print the title
        section_header = section_title.center(
            sum(col_width) + 2 * len(headers) + 4)
        print(section_header)

        # Print the table
        print(top_border)
        print(header_row)
        print(separator)

        # Display rows
        for row in rows:
            print(
                VR
                + VR.join(f" {row[i].center(col_width[i])} "
                          for i in range(len(headers)))
                + VR
            )
            print(bottom_border if row == rows[-1] else separator)

        if not rows:
            print(bottom_border)
            print("There are no recorded scores yet.")


class InputManager:
    """Represents the Input Component that is passed to the Game Class.

    It handles all input-related methods.
    """

    def __init__(self) -> None:
        pass

    def get_input(self, _input: str, valid_inputs: set[str]) -> list[str]:
        """Returns a list containing all the valid inputs of the player."""
        _input = _input.lower().strip()
        moves: list[str] = []

        for char in _input:
            if self.is_valid_input(char, valid_inputs):
                moves.append(char)

        return moves

    def is_valid_input(self, char: str, valid_inputs: set[str]) -> bool:
        """Checks whether an input is valid given a set of valid inputs."""
        return char.lower().strip() in {
            _input.lower().strip() for _input in valid_inputs
        }

    def get_moves_to_process(self, moves: Iterable,
                             moves_left: int) -> Generator:
        """Yields the moves to be processed given the remaining moves."""
        moves = iter(moves)

        for _ in range(moves_left):
            try:
                yield next(moves)
            except StopIteration:
                break


class ScoreManager:
    """Represents the Score Component that is passed to the Game Class.

    It basically has a setter and getter for the game score.
    """

    def __init__(self) -> None:
        """Initialize a private score variable and a list to keep track
        of score updates.
        """
        self._score = 0
        self.scores_list = [0]

    def set_score(self, score: int) -> None:
        """Hard set the current score."""
        self._score = score
        self.scores_list.append(self._score)

    def add_score(self, score: int) -> None:
        """Add to the current score."""
        self._score += score
        self.scores_list.append(self._score)

    def get_score(self) -> int:
        """Returns the current score."""
        return self._score
