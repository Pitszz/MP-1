from enum import Enum, auto


class GameState(Enum):
    PLAYING = auto()
    GAME_OVER = auto()
    LEADERBOARDS = auto()


class Direction(Enum):
    FORWARD = (-1, 0)
    BACKWARD = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class BlockType(Enum):
    IMMOVABLE = auto()
    MOVABLE = auto()
    FLOOR = auto()
    VOID = auto()
    GOAL = auto()


class Sprite():
    EGG = "🥚"
    WALL = "🧱"
    GRASS = "🟩"
    NEST = "🪹"
    FULL_NEST = "🪺"
    PAN = "🍳"
    HOLE = " "


class Config:
    ADD_SCORE = 10
    SUBSTRACT_SCORE = -5
    MOVE_DELAY = 0.4


BLOCK_MAP = {
    Sprite.EGG: ("Egg", BlockType.MOVABLE),
    Sprite.GRASS: ("Grass", BlockType.FLOOR),
    Sprite.WALL: ("Wall", BlockType.IMMOVABLE),
    Sprite.NEST: ("Nest", BlockType.GOAL),
    Sprite.FULL_NEST: ("Full Nest", BlockType.IMMOVABLE),
    Sprite.PAN: ("Pan", BlockType.VOID),
    Sprite.HOLE: ("Hole", BlockType.VOID),
}

DIRECTION_MAP = {
    "f": Direction.FORWARD,
    "b": Direction.BACKWARD,
    "l": Direction.LEFT,
    "r": Direction.RIGHT,
}

ARROW_MAP = {
    "f": "↑",
    "b": "↓",
    "l": "←",
    "r": "→",
}
