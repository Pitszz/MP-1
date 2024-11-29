def get_input(
    prompt: str, valid_inputs: list | tuple, is_game: bool = False
) -> list[str] | str:
    """Returns the valid inputs of the player as a list."""
    player_input = input(prompt).strip().lower()

    # Checks whether the input is actually a command
    if player_input.startswith("/"):
        stripped = player_input[1:].strip()
        if is_valid_input(stripped, valid_inputs):
            return stripped
        else:
            return None

    if is_valid_input(player_input, valid_inputs):
        return player_input

    # Do not process the input as moves if not on the playing state
    elif not is_game:
        return None

    # Otherwise, check for the valid moves
    movements = set("lfrb")
    moves = []

    for char in player_input:
        if is_valid_input(char, movements):
            moves.append(char)

    return moves


def is_valid_input(player_input: str, valid_inputs: set) -> bool:
    """Checks whether a given input is valid."""
    return player_input in set(str(valid).lower() for valid in valid_inputs)


def get_moves_to_process(moves: list[str], moves_left: int):
    """Yields the actual moves to be processed given the remaining moves."""
    moves = iter(moves)

    for _ in range(moves_left):
        try:
            yield next(moves)
        except StopIteration:
            break
