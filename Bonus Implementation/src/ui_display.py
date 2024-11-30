from src.ui_helper import convert_to_arrows, clear_screen, color, truncate, ENTER
from src.ui_colors import *
from src.config import MAX_STR, TITLE_DELAY, DELAY
from time import sleep


# Game displays


def update_display(level_data: dict) -> None:
    """Displays the current state of the grid along with the stats."""
    puzzle = level_data["puzzle"]

    clear_screen()
    display_stats(level_data)
    display_puzzle(puzzle)


def display_puzzle(grid: list[str]) -> None:
    """Prints the current state of the puzzle."""
    for row in grid:
        print("".join(row))


def display_stats(level_data: dict) -> None:
    """Displays the current status of the level."""
    points = sum(level_data["points"])
    moves_left = level_data["moves_left"]
    max_moves = level_data["max_moves"]
    undos_left = level_data["undos_left"]
    previous_moves = level_data["previous_moves"]
    previous_moves = convert_to_arrows(previous_moves)

    # Changes color of points text
    if points < 0:
        score_style = RED + BOLD
    else:
        score_style = GREEN + BOLD

    print(
        f"""
╭─────────────── {YELLOW + BOLD}LEVEL STATS{RESET} ─────────────╮
│ {YELLOW + BOLD}Points:         {RESET}{color(points, score_style)}{" " * (24 - len(str(points)))}│
│ {YELLOW + BOLD}Moves Left:     {RESET}{str(moves_left)}/{str(max_moves)}{" " * (23 - len(str(moves_left) + str(max_moves)))}│
│ {YELLOW + BOLD}Undos Left:     {RESET}{str(undos_left)}{" " * (24 - len(str(undos_left)))}│
│ {YELLOW + BOLD}Previous Moves: {RESET}{previous_moves}{" " * (24 - len(str(previous_moves)))}│
╰─────────────────────────────────────────╯
"""
    )


# Game menus


def display_main_menu() -> None:
    """Displays the main menu with buttons."""
    clear_screen()

    print(
        f"""
╭────────────────────────────────────────────────╮
│                                                │
│                  {color("< EGG ROLL >", YELLOW + BOLD)}                  │
│                                                │
│                 {color("╭────────────╮", GREEN + BOLD)}                 │
│                 {color("│    PLAY    │", GREEN + BOLD)}                 │
│                 {color("╰────────────╯", GREEN + BOLD)}                 │
│                 {color("╭────────────╮", GREEN + BOLD)}                 │
│                 {color("│    HELP    │", GREEN + BOLD)}                 │
│                 {color("╰────────────╯", GREEN + BOLD)}                 │
│             {color("╭────────────────────╮", GREEN + BOLD)}             │
│             {color("│    LEADERBOARDS    │", GREEN + BOLD)}             │
│             {color("╰────────────────────╯", GREEN + BOLD)}             │
│                 {color("╭────────────╮", RED + BOLD)}                 │
│                 {color("│    QUIT    │", RED + BOLD)}                 │
│                 {color("╰────────────╯", RED + BOLD)}                 │
│                                                │
╰────────────────────────────────────────────────╯
"""
    )


def display_help() -> None:
    """Displays the help section."""
    clear_screen()

    print(
        f"""{BOLD}╔════════════════════════════════════════════════╗
║               Egg Roll - How to Play           ║
╚════════════════════════════════════════════════╝{RESET}

→ Objective:
  - Roll eggs 🥚 into their nests 🪹
  - Avoid obstacles 🍳 that can crack your egg
  - Complete levels within limited moves

→ Controls:
  {color("[R]", GREEN + BOLD)} - → Right       {color("[L]", GREEN + BOLD)} - ← Left
  {color("[F]", GREEN + BOLD)} - ↑ Forward     {color("[B]", GREEN + BOLD)} - ↓ Backward

→ Other Commands: Add {YELLOW + BOLD}'/'{RESET} to avoid unwanted moves
  {color("[Undo]", RED + BOLD)} - Undo move  {color("[Reset]", RED + BOLD)} - Restart level
  
  {color("[Help]", YELLOW + BOLD)} - View Help  {color("[Board]", YELLOW + BOLD)} - View Leaderboards
  {color("[Quit]", YELLOW + BOLD)} - Exit game  {color("[Main]", YELLOW + BOLD)} - Go to Main Menu   
{BOLD}
╔════════════════════════════════════════════════╗
║        © Nathan Ramos & Ambernie Salting       ║
╚════════════════════════════════════════════════╝{RESET}"""
    )
    sleep(DELAY)
    input(f"\n→ Press {ENTER} to continue.")


# Level Selector


def display_table(headers: list[str], rows: list[str], section_title: str = "Table"):
    """Displays a dynamic table with given headers, rows, and a section title."""
    clear_screen()

    # Adjust col widths dynamically based on the longest str in each col
    all_rows = [headers] + rows
    col_width = [max(len(row[col]) for row in all_rows) for col in range(len(headers))]

    # Border styles
    TL, TR = "╭", "╮"
    BL, BR = "╰", "╯"
    HR, VR = "─", "│"
    MT, MB, ML, MR, MC = "┬", "┴", "├", "┤", "┼"

    # Horizontal borders
    top_border = TL + MT.join(HR * (width + 2) for width in col_width) + TR
    bottom_border = BL + MB.join(HR * (width + 2) for width in col_width) + BR
    separator = ML + MC.join(HR * (width + 2) for width in col_width) + MR

    # Header row
    header_row = (
        VR
        + VR.join(
            f" {BOLD}{headers[i].center(col_width[i])}{RESET} "
            for i in range(len(headers))
        )
        + VR
    )

    # Print the title
    section_header = section_title.center(sum(col_width) + 2 * len(headers) + 4)
    print(f"{YELLOW + BOLD}{section_header}{RESET}")

    # Print the table
    print(top_border)
    print(header_row)
    print(separator)

    # Display rows
    for row in rows:
        print(
            VR
            + VR.join(f" {row[i].center(col_width[i])} " for i in range(len(headers)))
            + VR
        )
        print(bottom_border if row == rows[-1] else separator)


def display_levels(levels: dict):
    headers = ["ID", "LEVEL NAME", "SIZE", "NOTE"]

    rows = [
        [
            f"{level_id:02}",
            truncate(level["name"], MAX_STR),
            level["size"],
            truncate(level["difficulty"], MAX_STR),
        ]
        for level_id, level in levels.items()
    ]

    display_table(headers, rows, "--- SELECT LEVEL ---")


def display_scoreboard(scoreboard: dict):
    headers = ["RANK", "NAME", "POINTS", "MOVES", "COMMENT"]
    sorted_scores = sorted(
        scoreboard["scores"], key=lambda x: (-x["points"], x["moves"], x["name"])
    )

    rows = [
        [
            f"{rank:02}",
            truncate(entry["name"], 25),
            str(entry["points"]),
            str(entry["moves"]),
            truncate(str(entry["comment"]), 100),
        ]
        for rank, entry in enumerate(sorted_scores, 1)
    ]

    display_table(headers, rows, f'--- Leaderboard: {scoreboard["level"]} ---')
    input(f"\n→ Press {ENTER} to go back to main menu.")


def display_leaderboards(rows: list[str]) -> None:
    headers = ["LEVEL", "NAME", "POINTS", "MOVES", "COMMENT"]

    display_table(headers, rows, f"--- Overall Leaderboards ---")
    input(f"\n→ Press {ENTER} to go back to main menu.")


# Title screen


def display_title() -> None:
    """Loads the title screen."""
    clear_screen()

    title = [
        r"  ______              _____       _ _ ",
        r" |  ____|            |  __ \     | | |",
        r" | |__   __ _  __ _  | |__) |___ | | |",
        r" |  __| / _` |/ _` | |  _  // _ \| | |",
        r" | |___| (_| | (_| | | | \ \ (_) | | |",
        r" |______\__, |\__, | |_|  \_\___/|_|_|",
        r"         __/ | __/ |                  ",
        r"        |___/ |___/                   ",
        "",
        " MP1: By Nathan Ramos & Ambernie Salting",
    ]

    for row in title:
        print(f"{YELLOW}{BOLD}{row}{RESET}")
        sleep(TITLE_DELAY)

    sleep(1)
