def get_moves(
    player_input: str,
    valid_inputs: set = ("help", "main", "quit"),
) -> list[str] | str | None:
    """Returns the valid inputs of the player as a list."""
    choice = str(player_input).strip().lower()

    # Checks whether the input is actually a command
    if choice.startswith("/"):
        stripped = choice[1:].strip()
        if is_valid_input(stripped, valid_inputs):
            return stripped
        else:
            return None

    if is_valid_input(choice, valid_inputs):
        return choice

    # Otherwise, check for the valid moves
    movements = set("lfrb")
    moves = []

    for char in choice:
        if is_valid_input(char, movements):
            moves.append(char)

    return moves


def get_input(
    player_input: str,
    valid_inputs: set = ("play", "help", "main", "quit"),
) -> None | str:
    """Returns the valid inputs of the player as a list."""
    choice = player_input.strip().lower()

    if is_valid_input(choice, valid_inputs):
        return choice
    else:
        return None


def is_valid_input(player_input: str, valid_inputs: set) -> bool:
    """Checks whether a given input is valid."""
    return player_input.strip().lower() in set(
        str(valid).lower() for valid in valid_inputs
    )


def get_moves_to_process(moves: list[str], moves_left: int):
    """Yields the actual moves to be processed given the remaining moves."""
    moves = iter(moves)

    for _ in range(moves_left):
        try:
            yield next(moves)
        except StopIteration:
            break
