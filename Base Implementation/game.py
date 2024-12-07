import os
import sys
import subprocess

from time import sleep


EGG = "🥚"
WALL = "🧱"
GRASS = "🟩"
NEST = "🪹"
FULL_NEST = "🪺"
PAN = "🍳"
VOID = " "


def main() -> None:
    """Main game loop."""
    initialize_game()

    filename = sys.argv[1]
    level_data = load_level(filename)

    while not is_end_state(level_data):
        # Update the display every frame
        update_display(level_data)

        moves_left = level_data["moves_left"]
        previous_moves = level_data["previous_moves"]

        controls = set("lrfb")
        player_input = get_input(input("Enter your move(s): "), controls)

        # Prompts the user again if there is no valid input
        if not player_input:
            print("No valid moves")
            sleep(0.5)
            continue

        # Collects all the valid moves within limited moves
        moves = [*get_moves_to_process(player_input, moves_left, previous_moves)]

        # Goes through all the moves
        for move in moves:
            level_data["current_move"] = move
            level_data["previous_moves"].append(move)
            process_move(move, level_data)
            level_data["moves_left"] -= 1

    game_over(level_data)


# Game Logic


def process_move(move: str, level_data: dict) -> None:
    """Continuously moves the eggs until all eggs are blocked."""
    # Maps the move to its respective direction increments
    increments = {"l": (0, -1), "r": (0, 1), "f": (-1, 0), "b": (1, 0)}
    direction = increments[move]

    puzzle = level_data["puzzle"]
    rows, cols = level_data["rows"], level_data["cols"]

    # Update display and move until the eggs cannot move further
    while not all_eggs_blocked(level_data, direction):
        clear_screen()
        puzzle = move_eggs(puzzle, direction, rows, cols, level_data)
        level_data["puzzle"] = puzzle

        display_puzzle(level_data["puzzle"])
        current_move = level_data["current_move"]
        print(f"Currently moving: {convert_to_arrows(current_move)}")
        sleep(0.35)


def move_eggs(
    grid: list[list[str]],
    direction: tuple[int, int],
    rows: int,
    cols: int,
    level_data: dict,
) -> list[list[str]]:
    """
    Handles the movement of the eggs dynamically for all direction by returning a new grid with updated positions.

    It also updates the scores accordingly.
    """
    (di, dj) = direction
    new_grid = [row[:] for row in grid]

    range_rows, range_cols = get_range(rows, cols, direction)

    for i in range_rows:
        for j in range_cols:
            if grid[i][j] == EGG:
                ni, nj = i + di, j + dj
                # Neighbor would be current pos of egg + increment
                if is_inside(ni, nj, rows, cols):
                    neighbor = new_grid[ni][nj]
                    if neighbor == GRASS:
                        new_grid[i][j] = GRASS
                        new_grid[ni][nj] = EGG
                    elif neighbor == NEST:
                        new_grid[i][j] = GRASS
                        new_grid[ni][nj] = FULL_NEST
                        level_data["points"].append(10 + level_data["moves_left"])
                    elif neighbor in (PAN, VOID):
                        new_grid[i][j] = GRASS
                        level_data["points"].append(-5)

    return new_grid


def all_eggs_blocked(level_data: dict, increment: list[int]) -> bool:
    """Returns True if all of the eggs cannot be moved further."""
    puzzle = level_data["puzzle"]
    rows, cols = level_data["rows"], level_data["cols"]
    eggs_pos = get_eggs_pos(puzzle)

    (di, dj) = increment
    for i, j in eggs_pos:
        # Checks the neighbor given an increment
        ni, nj = i + di, j + dj
        if is_inside(ni, nj, rows, cols):
            neighbor = puzzle[ni][nj]
            # We can move the egg still if the neighbor is grass, pan or empty nest
            if neighbor in set((GRASS, PAN, NEST)):
                return False

    return True


def is_inside(i: int, j: int, rows: int, cols: int) -> bool:
    """Checks whether the neigbor is inside the grid."""
    return 0 <= i < rows and 0 <= j < cols


def get_eggs_pos(grid: list[list[str]]) -> list[tuple]:
    """Returns all the current positions of the eggs."""
    result = []

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == EGG:
                result.append((row, col))

    return result


def get_range(rows: int, cols: int, direction: tuple[int, int]) -> tuple[range, range]:
    """Returns the corresponding iteration order of the rows and cols given a direction."""
    # Left & Up
    if direction in ((0, -1), (-1, 0)):
        return range(rows), range(cols)
    # Right & Down
    elif direction in ((0, 1), (1, 0)):
        return range(rows - 1, -1, -1), range(cols - 1, -1, -1)


# Initializers


def initialize_game() -> None:
    """Checks if a valid filename was given, otherwise it exits the program."""
    if len(sys.argv) < 2:
        print("The game requires a filename to start.", file=sys.stderr)
        sys.exit()
    else:
        file_path = os.path.join("levels", sys.argv[1])
        try:
            with open(file_path, encoding="utf-8") as file:
                pass
        except FileNotFoundError as error:
            print(error)
            sys.exit()

        print("Welcome to Egg Roll!")
        sleep(0.5)


def load_level(filename: str) -> None:
    """Given a filename, it stores the relevant information in a dictionary."""
    folder = "levels"
    file_path = os.path.join(folder, filename)

    level_data = {}
    try:
        with open(file_path, encoding="utf-8") as file:
            level_data["rows"] = int(file.readline())
            level_data["max_moves"] = int(file.readline())
            level_data["moves_left"] = level_data["max_moves"]
            level_data["puzzle"] = [
                list(file.readline().strip("\n")) for _ in range(level_data["rows"])
            ]
            level_data["cols"] = len(level_data["puzzle"][0])
    except FileNotFoundError as error:
        print(error)
        sys.exit()

    level_data["points"] = [0]
    level_data["previous_moves"] = []
    level_data["current_move"] = ""

    return level_data


# Display Functions


def update_display(level_data: dict) -> None:
    """Displays the current state of the grid along with the stats."""
    puzzle = level_data["puzzle"]

    clear_screen()
    display_puzzle(puzzle)
    display_stats(level_data)


def display_puzzle(grid: list[str]) -> None:
    """Prints the current state of the puzzle."""
    for row in grid:
        print("".join(row))


def display_stats(level_data: dict) -> None:
    """Prints the stats of the level."""
    points = sum(level_data["points"])
    max_moves = level_data["max_moves"]
    moves_left = level_data["moves_left"]
    previous_moves = level_data["previous_moves"]

    print(f"Points: {points}")
    print(f"Remaining moves: {moves_left}/{max_moves}")
    print(f"Previous moves: {convert_to_arrows(previous_moves, 20)}")


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


# Input Handling


def get_input(prompt: str, valid_inputs: list | tuple) -> list[str]:
    """Returns the valid inputs of the player as a list."""
    player_input = prompt.strip().lower()

    moves = []

    for char in player_input:
        if is_valid_input(char, valid_inputs):
            moves.append(char)

    return moves


def is_valid_input(player_input: str, valid_inputs: set) -> bool:
    """Checks whether a given input is valid."""
    return player_input in valid_inputs


def get_moves_to_process(moves: list[str], moves_left: int, previous_moves: list[str]):
    """Yields the moves to be processed given the remaining moves."""
    moves = iter(moves)

    for _ in range(moves_left):
        try:
            yield next(moves)
        except StopIteration:
            break


# End State


def is_end_state(level_data: dict) -> bool:
    """Returns true if there are no more eggs left or you have no more moves left."""
    moves_left = level_data["moves_left"]
    grid = level_data["puzzle"]

    if moves_left <= 0 or no_eggs_left(grid):
        return True
    else:
        return False


def no_eggs_left(grid: list[str]) -> bool:
    """Checks whether there are still eggs in the grid."""
    for row in grid:
        row = set(row)

        if EGG in row:
            return False

    return True


def game_over(level_data: dict) -> None:
    """Displays the final state of the grid and summary of the game."""
    points = sum(level_data["points"])
    puzzle = level_data["puzzle"]
    moves_played = level_data["previous_moves"]
    max_moves = level_data["max_moves"]
    moves_left = level_data["moves_left"]

    clear_screen()
    display_puzzle(puzzle)

    message = f"Congratulations! You got a total of {points} points!"
    if points < 0:
        message = f"Just keep on trying! You can turn that {points} points to positive!"

    print(message)
    print(f"Total moves done: {max_moves - moves_left}/{max_moves}")
    print(f"Moves played: {convert_to_arrows(moves_played)}")


# Helper Functions


def clear_screen() -> None:
    """Clears the terminal screen, if any"""
    if sys.stdout.isatty():
        clear_cmd = "cls" if os.name == "nt" else "clear"
        subprocess.run([clear_cmd], shell=True)


if __name__ == "__main__":
    main()
