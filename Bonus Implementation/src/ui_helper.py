import os
import sys
import subprocess

from src.ui_colors import *
from src.config import MOVE_DELAY
from time import sleep


INVALID = f"\n{RED + BOLD}< Invalid Input >{RESET}"
INVALID_LEVEL = f"\n{RED + BOLD}< Invalid Level ID >{RESET}"
YES_NO = f"{GREEN + BOLD}Y{RESET}/{RED + BOLD}N{RESET}"
ENTER = f"{BOLD}[Enter]{RESET}"


def clear_screen() -> None:
    """Clears the terminal screen, if any"""
    if sys.stdout.isatty():
        clear_cmd = "cls" if os.name == "nt" else "clear"
        subprocess.run([clear_cmd], shell=True)


def color(text: str | int, color: str) -> str:
    """Colorizes a text."""
    return f"{color}{str(text)}{RESET}"


def convert_to_arrows(previous_moves: list[str], max_length: int = 20) -> str:
    """Returns a string of converted moves to their respective arrow equivalent."""
    conversion = {
        "l": "←",
        "r": "→",
        "f": "↑",
        "b": "↓",
    }

    # This is to replace the string with '...←↑↓' in case it's too long
    converted = "".join([conversion[move] for move in previous_moves[-max_length:]])

    if len(previous_moves) > max_length:
        return "..." + converted
    else:
        return converted


def truncate(text: str, max_length: int) -> str:
    """Cuts down the string."""
    return text if len(text) <= max_length else text[: max_length - 3] + "..."


def fake_load(text: str, k: int) -> None:
    """Fake loading animation."""
    for i in range(k + 2):
        clear_screen()
        print(f"{text}" + "." * i)
        sleep(MOVE_DELAY)
