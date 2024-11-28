from src.ui_helper import convert_to_arrows, clear_screen, color, truncate, ENTER
from src.ui_colors import *
from time import sleep


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
    sleep(1)
    input(f"\n→ Press {ENTER} to continue.")


def display_levels(levels: dict) -> None:
    headers = ["ID", "NAME", "SIZE", "DIFFICULTY"]

    rows = []
    for level_id, level in levels.items():
        rows.append(
            [
                f"{level_id:02}",
                truncate(level["name"], 20),
                level["size"],
                truncate(level["difficulty"], 20),
            ]
        )

    all_rows = [headers] + rows
    col_width = [max(len(row[col]) for row in all_rows) for col in range(len(headers))]

    # Border style
    TL, TR = "╭", "╮"
    BL, BR = "╰", "╯"
    HR, VR = "─", "│"
    MT, MB, ML, MR, MC = "┬", "┴", "├", "┤", "┼"

    # Horizontal borders
    top_border = TL + MT.join(HR * (width + 2) for width in col_width) + TR
    bottom_border = BL + MB.join(HR * (width + 2) for width in col_width) + BR
    separator = ML + MC.join(HR * (width + 2) for width in col_width) + MR

    header_row = (
        VR
        + VR.join(
            f" {BOLD}{headers[i].center(col_width[i])}{RESET} "
            for i in range(len(headers))
        )
        + VR
    )

    # Display levels
    section_header = f"--- SELECT LEVEL ---".center(
        sum(col_width) + 2 * len(headers) + 4
    )

    print(f"{YELLOW + BOLD}{section_header}{RESET}")
    print(top_border)
    print(header_row)
    print(separator)

    for row in rows:
        print(
            VR
            + VR.join(f" {row[i].center(col_width[i])} " for i in range(len(headers)))
            + VR
        )
        print(bottom_border if row == rows[-1] else separator)
