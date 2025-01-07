from typing import Self, TYPE_CHECKING
from utils import Direction, Sprite, BlockType, Config, SPRITE_TO_BLOCK_TYPE


class Block:
    """Represents the Block Objects manipulated throughout the Game."""

    def __init__(self, name: str, sprite: str, _type: BlockType, row: int,
                 col: int):
        self.name: str = name
        self.sprite: str = sprite
        self.type: BlockType = _type
        self.row: int = row
        self.col: int = col

    def move(self, game, score_manager, moves_left, direction: Direction,
             idx: int) -> None:
        """Given a direction and index value, move the Movableto a new
        position based on the direction.
        """
        (i, j) = direction.value

        new_row: int = self.row + i
        new_col: int = self.col + j
        neighbor: Block = game.grid[new_row][new_col]

        self._on_collision(game, score_manager, new_row,
                           new_col, neighbor, moves_left, idx)

    def _on_collision(self, game, score_manager, new_row, new_col,
                      neighbor: Self, moves_left: int, idx: int) -> None:
        """Checks the neighbor of the Movable and determines what to do
        depending on its BlockType.
        """
        assert self.type == BlockType.MOVABLE

        match neighbor.type:
            # If neighbor is floor, simulate the movable moving by
            # changing its previous sprite to grass and changing the
            # new one to its sprite
            case BlockType.FLOOR:
                neighbor._change_block_to(Sprite.EGG)
                self._change_block_to(Sprite.GRASS)

                game.movables_positions[idx] = (new_row, new_col)

            # If neighbor is void, simulate the movable disappearing by
            # changing its sprite to grass and subtracting the score
            case BlockType.VOID:
                self._change_block_to(Sprite.GRASS)
                score_manager.add_score(Config.SUBSTRACT_SCORE)

                game.movables_index.append(idx)

            # If the neighbor is goal, change its sprite to full nest
            # and update the score depending on the moves left
            case BlockType.GOAL:
                neighbor._change_block_to(Sprite.FULL_NEST)
                self._change_block_to(Sprite.GRASS)
                score_manager.add_score(Config.ADD_SCORE + moves_left)

                game.movables_index.append(idx)

    def _change_block_to(self, sprite: str) -> None:
        """Changes the current block to another type given a sprite."""
        (name, blocktype) = SPRITE_TO_BLOCK_TYPE[sprite]

        self.sprite = sprite
        self.name = name
        self.type = blocktype
