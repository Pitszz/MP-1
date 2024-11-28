import os

from src.input_handler import get_input
from src.ui_display import display_levels
from src.ui_helper import clear_screen, fake_load, INVALID
from src.ui_colors import *
from time import sleep


def select_level(folder_name: str = "levels") -> dict:
    """Handles the level selection."""
    levels = get_all_levels(folder_name)
    levels_info = {idx: get_level_data(level) for (idx, level) in enumerate(levels, 1)}

    while True:
        clear_screen()
        display_levels(levels_info)

        prompt = f"\nChoose level {BOLD + BLUE}(1-{len(levels)}){RESET} ➤  "
        level_id = get_input(prompt, tuple(range(1, len(levels) + 1)))

        # Prompts again if chosen ID is invalid
        if level_id is None:
            print(INVALID)
            sleep(0.5)
            continue

        chosen_level = levels_info[int(level_id)]
        level_name = chosen_level["name"]
        fake_load(f"Loading: {GREEN + BOLD}{level_name}{RESET}", 2)

        return chosen_level


def get_all_levels(folder_name: str) -> list[str]:
    """Returns a list of all the files within a given folder."""
    levels = []

    for file_name in os.listdir(folder_name):
        if os.path.isfile(os.path.join(folder_name, file_name)):
            levels.append(file_name)

    return levels


def get_level_data(file_name: str, folder_name: str = "levels") -> dict:
    """Given a file_name, it extracts the data from it and returns it as a dictionary."""
    data = {}

    data["name"] = get_level_name(file_name)
    file_path = os.path.join(folder_name, file_name)

    try:
        with open(file_path, encoding="utf-8-sig") as file:
            data["rows"] = int(file.readline())
            data["max_moves"] = int(file.readline())
            data["moves_left"] = data["max_moves"]

            data["puzzle"] = [
                list(file.readline().strip()) for _ in range(data["rows"])
            ]
            data["cols"] = len(data["puzzle"][0])
            data["size"] = f"{data["rows"]}x{data["cols"]}"

            # Optional
            data["solution"] = file.readline().strip()
            data["difficulty"] = file.readline().strip()
            data["previous_states"] = [data["puzzle"]]

    except FileNotFoundError as error:
        print(f'File: "{file_name}" not found.')

    # MOVE SET
    data["current_move"] = ""
    data["previous_moves"] = []
    data["undos_left"] = 3

    # SCORE SET
    data["points"] = [0]

    # # For Debug
    # for (key, value) in data.items():
    #     print(key, value)

    return data


def get_level_name(file_name: str) -> str:
    """Returns the name of the file."""
    return file_name.split(".")[0].upper()


def undo_move(level_data: dict) -> None:
    previous_moves = level_data["previous_moves"]
    undos_left = level_data["undos_left"]

    if previous_moves and undos_left > 0:
        level_data["undos_left"] -= 1
        level_data["moves_left"] += 1
        level_data["points"].pop()
        level_data["previous_states"].pop()
        level_data["previous_moves"].pop()
        level_data["puzzle"] = level_data["previous_states"][-1]
    elif undos_left <= 0:
        print(f"\n{RED + BOLD}< No more undos left >{RESET}")
        sleep(0.5)
    elif not previous_moves:
        print(f"\n{RED + BOLD}< Nothing to undo >{RESET}")
        sleep(0.5)


def restart_game(level_data: dict) -> None:
    level_data["undos_left"] = 3
    level_data["moves_left"] = level_data["max_moves"]
    level_data["points"] = [0]
    level_data["previous_moves"].clear()
    level_data["puzzle"] = level_data["previous_states"][0]
    level_data["previous_states"] = level_data["previous_states"][0]
