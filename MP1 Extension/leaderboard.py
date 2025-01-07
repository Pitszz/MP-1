import os
import json

from utils import Path


class Leaderboard:
    """Represents the Leaderboard for the Game.

    It handles the creation of the directory and files for
    the leaderboard. It also manages the updating of existing
    leaderboards.
    """

    def __init__(self) -> None:
        pass

    def initialize_leaderboard(self, filename: str, folder_name: str) -> None:
        """Creates the directory and leaderboard file at the game
        loadup.
        """
        default_leaderboard = {"level": filename, "scores": []}
        json_name = f"{filename}_leaderboard.json"

        self._create_folder(folder_name)
        self.create_json_file(json_name, default_leaderboard, folder_name)

    def get_leaderboard(self, json_file: str,
                        folder_name: str = Path.LEADERBOARDS_FOLDER) -> dict:
        """Returns the current data of a leaderboard file as a
        dictionary.
        """
        json_path = os.path.join(folder_name, json_file)

        # Check if the file exists
        if not os.path.exists(json_path):
            raise FileNotFoundError(
                f"File: {json_file} does not exist."
            )

        # Load and return the content of the file
        with open(json_path, "r") as file:
            data = json.load(file)

        return data

    def _create_folder(self, folder_name: str) -> None:
        """Creates a folder given a name, if it doesn't exist yet."""
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    def create_json_file(self, filename: str, content: dict,
                         folder_name: str = Path.LEADERBOARDS_FOLDER) -> None:
        """Creates a json file and stores in it a default data, if it
        doesn't exist yet.
        """
        json_path = os.path.join(folder_name, filename)

        if not os.path.exists(json_path):
            with open(json_path, "w") as json_file:
                json.dump(content, json_file, indent=4)

    def add_to_leaderboard(self, filename: str, name: str, score: int,
                           moves: int) -> None:
        """Updates the current leaderboard with a new entry."""
        to_add = {"name": name, "score": score, "moves": moves}

        filename = f"{filename}_leaderboard.json"
        leaderboard = self.get_leaderboard(filename)
        leaderboard["scores"].append(to_add)

        json_path = os.path.join(Path.LEADERBOARDS_FOLDER, filename)

        if os.path.exists(json_path):
            with open(json_path, "w") as json_file:
                json.dump(leaderboard, json_file, indent=4)
        else:
            raise FileNotFoundError(
                f"File: {json_path} does not exist."
            )
