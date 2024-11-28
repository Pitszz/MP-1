import sys

from src.core_logic import process_move, is_end_state
from src.input_handler import get_input, get_moves_to_process
from src.level_manager import select_level, undo_move, restart_game
from src.ui_display import (
    update_display,
    display_main_menu,
    display_help,
    display_puzzle,
)
from src.ui_helper import clear_screen, convert_to_arrows, INVALID, YES_NO, ENTER
from src.ui_colors import *
from time import sleep


def initialize_game() -> None:
    pass


def main_menu() -> str:
    while True:
        display_main_menu()

        commands = ("play", "help", "leaderboards", "board", "quit", "exit")
        player_input = get_input("➤  ", commands)

        if player_input is not None:
            return player_input
        else:
            print(INVALID)
            sleep(0.5)


def play_game() -> None:
    level_data = select_level("levels")

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
        previous_moves = level_data["previous_moves"]

        prompt = f"\nEnter your {BLUE + BOLD}move(s){RESET} ➤  "
        player_input = get_input(prompt, commands, is_game=True)

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
                level_data["moves_left"] -= 1
                level_data["current_move"] = move
                level_data["previous_moves"].append(move)
                process_move(move, level_data)

        # Prompts the user again if there is no valid input
        elif not player_input:
            print(INVALID)
            sleep(0.5)

    game_over(level_data)


def _process_command(command: str, level_data: dict) -> None:
    """Helper function to process the given command."""
    if command == "help":
        display_help()
    elif command in ("leaderboards", "board"):
        leaderboards()
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
    pass


def exit_game() -> None:
    """Prompts the user if they want to quit the game or not."""
    while True:
        clear_screen()

        prompt = f"Are you sure you want to quit? ({YES_NO}): "
        player_input = get_input(prompt, ("yes", "y", "no", "n"))

        if player_input in ("yes", "y"):
            sys.exit()
        elif player_input in ("no", "n"):
            return
        elif player_input is None:
            print(INVALID)
            sleep(0.5)


def game_over(level_data: dict) -> None:
    """Displays the final state of the grid and summary of the game."""
    update_display(level_data)
    points = sum(level_data["points"])

    message = (
        f"Congratulations! You got a total of {BOLD + GREEN}{points}{RESET} points!"
    )
    if points < 0:
        message = f"Just keep on trying! You can turn that {BOLD + RED}{points}{RESET} points to positive!"

    print(f"\n{message}")
    sleep(0.5)
    input(f"\n→ Press {ENTER} to go back to main menu.")
