import os
import json

from src.level_manager import get_all_levels, get_level_name
from src.config import BOARD_DIR, LEVEL_DIR


def initialize_leaderboards() -> None:
    """Creates a directory and all the scoreboard files."""
    _create_directory(BOARD_DIR)

    for level in get_all_levels(LEVEL_DIR):
        _create_file(BOARD_DIR, level)


def _create_directory(directory: str) -> None:
    """Creates a leaderboards folder if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")


def _create_file(directory: str, level: str) -> None:
    """
    Creates a JSON file for a given level if it doesn't exist,
    and initializes it with the default scoreboard.
    """
    level = get_level_name(level)
    json_path = os.path.join(directory, f"{level}_scoreboard.json")

    DEFAULT_SCOREBOARD = {
        "level": level,
        "scores": [],
    }

    if not os.path.exists(json_path):
        with open(json_path, "w") as json_file:
            json.dump(DEFAULT_SCOREBOARD, json_file, indent=4)
        print(f"Initialized scoreboard for {level}: {json_path}")
    else:
        print(f"Scoreboard already exists for {level}: {json_path}")


def access_scoreboard(name: str) -> dict:
    json_path = os.path.join(BOARD_DIR, f"{name}_scoreboard.json")

    # Check if the file exists
    if not os.path.exists(json_path):
        raise FileNotFoundError(
            f"Scoreboard file for '{name}' does not exist at {json_path}."
        )

    # Load and return the content of the file
    with open(json_path, "r") as json_file:
        data = json.load(json_file)

    return data


def add_to_scoreboard(
    level: str, name: str, points: int, moves: int, comment: str
) -> None:
    to_add = {"name": name, "points": points, "moves": moves, "comment": comment}

    scoreboard = access_scoreboard(level)
    scoreboard["scores"].append(to_add)

    json_path = os.path.join(BOARD_DIR, f"{level}_scoreboard.json")

    # Save the updated scoreboard back to the file
    with open(json_path, "w") as json_file:
        json.dump(scoreboard, json_file, indent=4)
