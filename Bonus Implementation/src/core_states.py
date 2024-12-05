import sys

from src.core_logic import process_move, is_end_state
from src.input_handler import get_input, get_moves_to_process, get_moves
from src.level_manager import (
    select_level,
    undo_move,
    restart_game,
    get_count,
    get_all_levels,
    get_level_name,
)
from src.leaderboards import (
    initialize_leaderboards,
    access_scoreboard,
    add_to_scoreboard,
)
from src.ui_display import (
    display_title,
    update_display,
    display_main_menu,
    display_help,
    display_scoreboard,
    display_leaderboards,
)
from src.ui_helper import clear_screen, truncate, INVALID, YES_NO, ENTER
from src.ui_colors import *
from src.config import *
from time import sleep


def initialize_game() -> None:
    """Displays the title screen and help section."""
    initialize_leaderboards()
    display_title()
    display_help()


def main_menu() -> str:
    """Main menu section."""
    while True:
        display_main_menu()

        commands = ("play", "help", "leaderboards", "board", "quit", "exit")
        player_input = get_input(input("➤  "), commands)

        if player_input is not None:
            return player_input
        else:
            print(INVALID)
            sleep(DELAY)


def play_game() -> None:
    """Handles the playing state."""
    level_data = select_level(LEVEL_DIR)

    commands = (
        "help",
        "main",
        "leaderboards",
        "board",
        "quit",
        "exit",
        "undo",
        "restart",
        "reset",
        "solution",
    )

    while not is_end_state(level_data):
        # Update the display every frame
        update_display(level_data)

        moves_left = level_data["moves_left"]

        prompt = f"\nEnter your {BLUE + BOLD}move(s){RESET} ➤  "
        player_input = get_moves(input(prompt), commands)

        # Checks whether the input is a command
        if player_input in commands:
            if player_input == "main":
                return  #  Go back to main menu
            elif player_input == "undo":
                undo_move(level_data)
                continue
            elif player_input == "reset":
                restart_game(level_data)
                continue

            _process_command(player_input, level_data)

        # Checks if the input are movements
        elif isinstance(player_input, list) and player_input:
            # Collects all the valid moves given the remaining moves
            moves = [*get_moves_to_process(player_input, moves_left)]

            # Process each move
            for move in moves:
                level_data["current_move"] = move
                process_move(move, level_data)
                level_data["previous_moves"].append(move)
                level_data["moves_left"] -= 1

        # Prompts the user again if there is no valid input
        elif not player_input:
            print(INVALID)
            sleep(DELAY)

    game_over(level_data)


def _process_command(command: str, level_data: dict) -> None:
    """Helper function to process the given command."""
    if command == "help":
        display_help()
    elif command in ("leaderboards", "board"):
        scoreboard(level_data["name"])
    elif command in ("quit", "exit"):
        exit_game()
    elif command == "solution":
        solution = level_data["solution"].strip()

        if not solution:
            solution = "No available solution"
            print(f"\nSolution: {BOLD + RED}{solution.upper()}{RESET}")
        else:
            print(f"\nSolution: {BOLD + GREEN}{solution.upper()}{RESET}")

        input(f"\n→ Press {ENTER} to return to game.")


def leaderboards() -> None:
    """Displays the overall leaderboard."""
    rows = []

    for level in get_all_levels(LEVEL_DIR):
        level_name = get_level_name(level)
        board = access_scoreboard(level_name)

        # Get the first rank for the level
        if board["scores"]:
            topper = sorted(
                board["scores"], key=lambda x: (-x["points"], x["moves"], x["name"])
            )[0]
        # Load a blank row if no scores available yet
        else:
            topper = {
                "name": "",
                "points": "",
                "moves": "",
                "comment": "",
            }

        rows.append(
            [
                level_name,
                truncate(topper["name"], 25),
                str(topper["points"]),
                str(topper["moves"]),
                truncate(topper["comment"], 100),
            ]
        )

    display_leaderboards(rows)


def scoreboard(name: str = None) -> None:
    """Displays the current scoreboard for a level."""
    board = access_scoreboard(name)

    # If no leaderboard yet, don't print the table
    if not board["scores"]:
        print(f"\n{RED + BOLD}< No scores available yet >{RESET}")
        sleep(DELAY)
        return

    display_scoreboard(board)


def exit_game() -> None:
    """Prompts the user if they want to quit the game or not."""
    while True:
        clear_screen()

        prompt = f"Are you sure you want to quit? ({YES_NO}): "
        player_input = get_input(input(prompt), ("yes", "y", "no", "n"))

        if player_input in ("yes", "y"):
            sys.exit()
        elif player_input in ("no", "n"):
            return
        elif player_input is None:
            print(INVALID)
            sleep(DELAY)


def game_over(level_data: dict) -> None:
    """Displays the final state of the grid and summary of the game."""
    update_display(level_data)

    # Score summary
    points = sum(level_data["points"])
    message = (
        f"Congratulations! You got a total of {BOLD + GREEN}{points}{RESET} points"
    )

    print(
        f"\n{message} in {BLUE + BOLD}{len(level_data["previous_moves"])}{RESET} moves!"
    )

    # Egg summary
    total_eggs = level_data["egg_count"]
    nested_eggs = get_count(level_data["puzzle"], FULL_NEST)

    print(
        f"\nYou guided {BOLD + YELLOW}{nested_eggs}{RESET} egg(s) out of {BOLD + YELLOW}{total_eggs}{RESET}"
    )

    sleep(DELAY)

    # Add to leaderboard prompt
    while True:
        prompt = f"\nWould you like to add yourself to the leaderboard? ({YES_NO}): "
        player_input = get_input(input(prompt), ("yes", "no", "n", "y"))

        if player_input in ("yes", "y"):
            level_name = level_data["name"]
            name = input(f"\nEnter your {BOLD + BLUE}name{RESET}: ").strip()
            points = sum(level_data["points"])
            moves = len(level_data["previous_moves"])
            comment = input(f"Add a {BOLD + BLUE}comment{RESET}: ").strip()
            player_info = (name, points, moves, comment)

            # Update the scoreboard with the info provided
            add_to_scoreboard(level_name, *player_info)
            scoreboard = access_scoreboard(level_name)

            # Display the updated scoreboard
            display_scoreboard(scoreboard)
            break
        elif player_input in ("no", "n"):
            break
        elif player_input is None:
            print(INVALID)
            sleep(DELAY)
            game_over(level_data)
            break
