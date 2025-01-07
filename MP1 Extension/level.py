import os
import sys
import copy

from utils import BlockType, SPRITE_TO_BLOCK_TYPE
from block import Block


class Level:
    """Represents a Level Object.

    It gathers all the data stored in a specific file. It creates
    a grid filled with Block Objects based on information from the
    sprite in connection with utils.py
    """

    def __init__(self) -> None:
        self._grid: list[list[Block]] = []
        self._max_moves: int = 0
        self._movables_positions: list[tuple] = []
        self.rows: int = 0
        self.cols: int = 0
        self.level_name: str = ""

    def load_level(self, filename: str, folder: str) -> None:
        """Given a filename, reads the stage data inside the file and
        generates a grid with Block objects.
        """
        file_path = os.path.join(folder, filename)
        self.level_name = self.get_level_name(filename)

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.rows = int(file.readline())
                self._max_moves = int(file.readline())

                for row in range(self.rows):
                    line = file.readline().strip('\n')
                    grid_row = [
                        self._create_block(sprite, row, col)
                        for (col, sprite) in enumerate(line)
                    ]
                    self._grid.append(grid_row)

                self.cols = len(self._grid[0])

        except FileNotFoundError:
            print(f"File {filename} not found")
            sys.exit()

    def _create_block(self, sprite: str, row: int, col: int) -> Block:
        """
        Creates a Block object that has a given set of attributes
        based on the name, Sprite, BlockType andposition in the grid.
        """
        (name, block_type) = SPRITE_TO_BLOCK_TYPE[sprite]

        # Store all of the movable positions
        if block_type == BlockType.MOVABLE:
            self._movables_positions.append((row, col))

        return Block(name, sprite, block_type, row, col)

    def get_initial_grid(self) -> list[list[Block]]:
        """Returns a copy the initial state of the grid."""
        grid_copy = copy.deepcopy(self._grid)

        return grid_copy

    def get_max_moves(self) -> int:
        """Returns the maximum number of moves for the level."""
        return self._max_moves

    def get_movables_positions(self) -> list[tuple]:
        """Returns a copy of the  positions of movable objects in the
        grid.
        """
        return self._movables_positions[:]

    def get_level_name(self, filename: str) -> str:
        """Returns the name of the level."""
        dot_idx = filename[::-1].index(".")

        return filename[: -(dot_idx + 1)].title()
