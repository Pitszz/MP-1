import pytest

from src.input_handler import get_input, get_moves, get_moves_to_process, is_valid_input


def test_get_moves() -> None:
    commands = (
        "main",
        "help",
        "leaderboards",
        "board",
        "exit",
        "quit",
        "undo",
        "reset",
        "restart",
    )

    # Normal input
    assert get_moves("LFRB", commands) == ["l", "f", "r", "b"]
    assert get_moves("     R     L      l    k   b ", commands) == ["r", "l", "l", "b"]
    assert get_moves("", commands) == []
    assert get_moves("llll", commands) == ["l", "l", "l", "l"]
    assert get_moves("lfrb" * 10, commands) == ["l", "f", "r", "b"] * 10
    assert get_moves("12345678") == []

    # Commands
    assert get_moves("main", commands) == "main"
    assert get_moves("/help", commands) == "help"
    assert get_moves(" /CHICKEN", commands) == None
    assert get_moves(" /          main", commands) == "main"
    assert get_moves("/BoArD", commands) == "board"

    # Starts with '/'
    assert get_moves("//////", commands) == None
    assert get_moves("/LR", commands) == None
    assert get_moves("/Egg Roll") == None

    # Random words
    assert get_moves("          THIS IS HOW YOU DO IT          ", commands) == []
    assert get_moves("k k k", commands) == []
    assert get_moves("cdrcler", commands) == ["r", "l", "r"]
    assert get_moves("SKYDIVER", commands) == ["r"]
    assert get_moves("fluffy", commands) == ["f", "l", "f", "f"]
    assert get_moves("iwanttodropbuticant", commands) == ["r", "b"]
    assert get_moves("mother mary, comes to me", commands) == ["r", "r"]
    assert get_moves("thoughtcrime", commands) == ["r"]
    assert get_moves("karasu no uta ni akane", commands) == ["r"]
    assert get_moves("ich bin ein berliner", commands) == ["b", "b", "r", "l", "r"]
    assert get_moves("Embodiment of Scarlet Devil", commands) == [
        "b",
        "f",
        "r",
        "l",
        "l",
    ]
    assert get_moves("it is what it is", commands) == []
    assert get_moves(
        "Hey guys, did you know that in terms of male human and female Pokemon breeding...",
        commands,
    ) == ["r", "f", "l", "f", "l", "b", "r"]
    assert get_moves("The Game", commands) == []
    assert get_moves("You just lost the game.", commands) == ["l"]


def test_get_input() -> None:
    commands = ("play", "help", "quit", "exit", "leaderboards", "board")

    assert get_input("help", commands) == "help"
    assert get_input("qUiT   ", commands) == "quit"
    assert get_input("  EXIT  ", commands) == "exit"


def test_get_moves_to_process() -> None:
    # This takes in pre-processed input (valid list) and yields the actual moves to be processed given remaining moves
    assert [*get_moves_to_process(["l", "r", "l", "l"], 3)] == ["l", "r", "l"]
    assert [*get_moves_to_process(["f", "r", "b", "l"] * 10, 3)] == ["f", "r", "b"]
    assert [*get_moves_to_process(["l", "r"], 10)] == ["l", "r"]
    assert [*get_moves_to_process(["l", "r", "f", "b"], 0)] == []


def test_is_valid_input() -> None:
    commands = ("play", "help", "quit", "exit", "leaderboards", "board")

    assert is_valid_input("play", commands) == True
    assert is_valid_input("HELP", commands) == True
    assert is_valid_input("chicken", commands) == False
    assert is_valid_input("12345", commands) == False

    # Random
    assert is_valid_input("/ / / / ", commands) == False
    assert is_valid_input(".....", commands) == False
    assert is_valid_input("   ", commands) == False
