from src.core_states import (
    initialize_game,
    main_menu,
    play_game,
    display_help,
    leaderboards,
    exit_game,
)


def main() -> None:
    """Main game loop."""

    initialize_game()

    current_state = "main_menu"

    # State handling
    while True:
        if current_state == "main_menu":
            current_state = main_menu()
            continue

        elif current_state == "play":
            play_game()

        elif current_state == "help":
            display_help()

        elif current_state in ("leaderboards", "board"):
            leaderboards()

        elif current_state in ("quit", "exit"):
            exit_game()

        # Go back to main menu
        current_state = "main_menu"


if __name__ == "__main__":
    main()
