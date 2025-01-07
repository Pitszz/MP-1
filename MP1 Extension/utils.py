from enum import Enum, auto


class Config:
    """Contains the configuration values for the game."""
    ADD_SCORE = 10
    SUBSTRACT_SCORE = -5
    MOVE_DELAY = 0.4

    # Input
    PROMPT = "Enter your move: "
    VALID_INPUTS = set("fblr")
    EXIT_COMMANDS = set(["~quit", "~exit", "~q"])
    LEADERBOARD_COMMANDS = set(["~leaderboard", "~board"])


class Path:
    """Contains all the paths to the respective game folders."""
    LEVELS_FOLDER = "levels"
    LEADERBOARDS_FOLDER = "leaderboards"


class GameState(Enum):
    """[Enum] Represents the different states of the game."""
    PLAYING = auto()
    GAME_OVER = auto()
    LEADERBOARDS = auto()


class Direction(Enum):
    """[Enum] Represents the four movement directions."""
    FORWARD = (-1, 0)
    BACKWARD = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


# For Extendability, you can easily create new types of blocks by
# adding blocktypes and sprites and making sure it is updated in the
# SPRITE_TO_BLOCK_TYPE dictionary and handle the behaviors on the
# _on_collision method of the Block Class

class BlockType(Enum):
    """[Enum] Represents the different types of blocks."""
    MOVABLE = auto()
    GOAL = auto()
    IMMOVABLE = auto()
    FLOOR = auto()
    VOID = auto()


class Sprite:
    """Contains the sprites of each block."""
    EGG = "🥚"
    FULL_NEST = "🪺"
    NEST = "🪹"
    WALL = "🧱"
    GRASS = "🟩"
    PAN = "🍳"
    HOLE = " "


SPRITE_TO_BLOCK_TYPE = {
    Sprite.EGG: ("Egg", BlockType.MOVABLE),
    Sprite.NEST: ("Nest", BlockType.GOAL),
    Sprite.FULL_NEST: ("Full Nest", BlockType.IMMOVABLE),
    Sprite.WALL: ("Wall", BlockType.IMMOVABLE),
    Sprite.GRASS: ("Grass", BlockType.FLOOR),
    Sprite.PAN: ("Pan", BlockType.VOID),
    Sprite.HOLE: ("Hole", BlockType.VOID),
}

INPUT_TO_DIRECTION = {
    "f": Direction.FORWARD,
    "b": Direction.BACKWARD,
    "l": Direction.LEFT,
    "r": Direction.RIGHT,
}

MOVE_TO_ARROW = {
    "f": "↑",
    "b": "↓",
    "l": "←",
    "r": "→",
}
