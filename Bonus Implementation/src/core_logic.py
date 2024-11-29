from src.ui_display import update_display
from src.ui_helper import clear_screen, convert_to_arrows
from src.ui_colors import *
from time import sleep


EGG = "🥚"
WALL = "🧱"
GRASS = "🟩"
NEST = "🪹"
FULL_NEST = "🪺"
PAN = "🍳"
VOID = " "


def process_move(move: str, level_data: dict) -> None:
    """Continuously moves the eggs until all eggs are blocked."""
    # Maps the move to its respective direction increments
    increments = {"l": (0, -1), "r": (0, 1), "f": (-1, 0), "b": (1, 0)}
    direction = increments[move]

    puzzle = level_data["puzzle"]
    rows, cols = level_data["rows"], level_data["cols"]

    score_per_move = 0
    # Update display and move until the eggs cannot move further
    while not all_eggs_blocked(level_data, direction):
        clear_screen()
        (puzzle, score) = move_eggs(puzzle, direction, rows, cols, level_data)
        score_per_move += score
        level_data["puzzle"] = puzzle

        update_display(level_data)
        current_move = level_data["current_move"]
        print(
            f"\nCurrently moving: {BOLD + GREEN}{convert_to_arrows(current_move)}{RESET}"
        )
        sleep(0.35)

    # Only add the score once the move has finished
    level_data["points"].append(score_per_move)
    level_data["previous_states"].append(puzzle)


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
    temp_score = 0

    for i in range_rows:
        for j in range_cols:
            if grid[i][j] == EGG:
                ni, nj = i + di, j + dj
                if is_inside(ni, nj, rows, cols):
                    # Neighbor would be current pos of egg + increment
                    neighbor = new_grid[ni][nj]

                    # EGG -> GRASS
                    if neighbor == GRASS:
                        new_grid[i][j] = GRASS
                        new_grid[ni][nj] = EGG

                    # EGG -> NEST
                    elif neighbor == NEST:
                        new_grid[i][j] = GRASS
                        new_grid[ni][nj] = FULL_NEST
                        temp_score += 5 + level_data["moves_left"]

                    # EGG -> PAN
                    elif neighbor in (PAN, VOID):
                        new_grid[i][j] = GRASS
                        temp_score -= 5

    return new_grid, temp_score


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
            if neighbor in set((GRASS, PAN, NEST, VOID)):
                return False

    return True


def is_inside(i: int, j: int, rows: int, cols: int) -> bool:
    """Checks whether the object is inside the grid."""
    return 0 <= i < rows and 0 <= j < cols


def get_eggs_pos(grid: list[list[str]]) -> list[int]:
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


# End State


def is_end_state(level_data: dict) -> bool:
    """Returns true if there are no more eggs left or you have no more moves left."""
    moves_left = level_data.get("moves_left", 0)
    grid = level_data.get("puzzle", None)

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
