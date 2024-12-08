import pytest
from random import randint
from src.input_handler import get_input, get_moves, get_moves_to_process, is_valid_input
from src.ui_helper import convert_to_arrows


def test_get_moves() -> None:
    # Takes in an INPUT (str) from the user -> returns a LIST of all the valid moves (or None) or a STR if it's a command
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
        "solution"
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
    assert get_moves(" m a i n ", commands) == []
    assert get_moves(" solution ", commands) == "solution"  # Backdoor
    assert get_moves("/help", commands) == "help"
    assert get_moves(" /CHICKEN", commands) == None
    assert get_moves(" /          main", commands) == "main"
    assert get_moves("/BoArD", commands) == "board"

    # Starts with '/'
    assert get_moves("//////", commands) == None
    assert get_moves("/LR", commands) == None
    assert get_moves("/Egg Roll", commands) == None
    assert get_moves("/ s olution", commands) == None

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
    assert get_moves("Embodiment of Scarlet Devil", commands) == ["b", "f", "r", "l", "l"]
    assert get_moves("it is what it is", commands) == []
    assert get_moves(
        "Hey guys, did you know that in terms of male human and female Pokemon breeding...",
        commands,
    ) == ["r", "f", "l", "f", "l", "b", "r"]
    assert get_moves("The Game", commands) == []
    assert get_moves("You just lost the game.", commands) == ["l"]
    assert get_moves("Life does indeed find a way to f--- you over.", commands) == ["l", "f", "f", "f", "r"]
    assert get_moves("But be happy that you're alive today.", commands) == ["b", "b", "r", "l"]


    # EDGE CASES

    # Empty Input
    assert get_moves("", commands) == []

    # Really Large Input, (same characters)
    assert get_moves("l" * 10**6, commands) == ["l"] * 10**6

    mock_input = mock_moves_list_gen(10**6)
    # Really Large Input, (different characters) 
    assert get_moves(''.join(mock_input), commands) == mock_input


def test_get_input() -> None:
    # Takes in an INPUT (str) -> returns a STR if it's a valid command, NONE otherwise
    # Used for all other prompts besides the gameplay state
    commands = ("play", "help", "quit", "exit", "leaderboards", "board")

    assert get_input("help", commands) == "help"
    assert get_input("qUiT   ", commands) == "quit"
    assert get_input("  EXIT  ", commands) == "exit"
    assert get_input(" NONE ", commands) == None


def test_get_moves_to_process() -> None:
    # This takes in a VALID LIST of STR (PRE-PROCESSED INPUT) of moves and yields the actual moves to be processed given remaining moves
    assert [*get_moves_to_process(["l", "r", "l", "l"], 3)] == ["l", "r", "l"]
    assert [*get_moves_to_process(["f", "r", "b", "l"] * 10, 3)] == ["f", "r", "b"]
    assert [*get_moves_to_process(["l", "r"], 10)] == ["l", "r"]
    assert [*get_moves_to_process(["l", "r", "f", "b"], 0)] == []
    assert [*get_moves_to_process(["l", "r", "f", "b"], 20)] == ["l", "r", "f", "b"]
    assert [*get_moves_to_process(["l", "r", "f", "b"] * 5, 10)] == ["l", "r", "f", "b"] * 2 + ["l", "r"]
    assert [*get_moves_to_process(["b", "b", "b", "b"], 1)] == ["b"]
    assert [*get_moves_to_process(["l", "l", "r", "f", "b"], 4)] == ["l", "l", "r", "f"]
    assert [*get_moves_to_process(["l", "r", "f", "b", "l", "f"], 2)] == ["l", "r"]

    #EDGE CASES

    # Negative moves left. Unlikely to happen in-game, but it doesn't hurt to try.
    assert [*get_moves_to_process(["l", "r", "l", "l"], -1)] == []

    # No moves to process. Unlikely to happen in-game as well.
    assert [*get_moves_to_process([], 3)] == []

    # No moves to process & negative moves. (If this happens in-game, the player is a wizard...)
    assert [*get_moves_to_process([], -1)] == []

    # Large Inputs, varying amounts of remaining moves
    assert [*get_moves_to_process(["l"] * 10**6, 0)] == []
    assert [*get_moves_to_process(["l"] * 10**6, 1)] == ["l"]
    assert [*get_moves_to_process(["l"] * 10**6, 100)] == ["l"] * 100
    assert [*get_moves_to_process(["l"] * 10**6, 10**5)] == ["l"] * 10**5
    assert [*get_moves_to_process(["l", "r"] * 10**6, 10**5)] == ["l", "r"] * ((10**5) // 2)
    assert [*get_moves_to_process(["l", "r"] * 10**6, 10)] == ["l", "r"] * 5

    # Using lists comprehension to generate large inputs with random moves.
    # Upper limit with the code is 10**7, it slows down significantly around the 10**6 mark.
    mock_moves_list_1 = mock_moves_list_gen(10**5)
    mock_moves_list_2 = mock_moves_list_gen(10**6) # slows down the test by ~1 second
    mock_moves_list_3 = mock_moves_list_gen(10**7) # slows down the test by ~5 seconds
    # to the tester, don't try 10**8 & above, it'll probably take minutes (i tested & it took about a minute...)

    assert [*get_moves_to_process(mock_moves_list_1, 0)] == []
    assert [*get_moves_to_process(mock_moves_list_2, 0)] == []
    assert [*get_moves_to_process(mock_moves_list_3, 0)] == []
    assert [*get_moves_to_process(mock_moves_list_1, 10)] == mock_moves_list_1[:10]
    assert [*get_moves_to_process(mock_moves_list_2, 10)] == mock_moves_list_2[:10]
    assert [*get_moves_to_process(mock_moves_list_3, 10)] == mock_moves_list_3[:10]
    assert [*get_moves_to_process(mock_moves_list_1, 100)] == mock_moves_list_1[:100]
    assert [*get_moves_to_process(mock_moves_list_2, 100)] == mock_moves_list_2[:100]
    assert [*get_moves_to_process(mock_moves_list_3, 100)] == mock_moves_list_3[:100]
    assert [*get_moves_to_process(mock_moves_list_3, 10**8)] == mock_moves_list_3


def test_is_valid_input() -> None:
    # Takes an INPUT (str) -> returns a BOOL whether it is in the list of valid commands
    commands = ("play", "help", "quit", "exit", "leaderboards", "board")

    def mock_func():
        def mock_func_in():
            pass

        return mock_func_in

    assert is_valid_input("play", commands)
    assert is_valid_input("HELP", commands)
    assert is_valid_input("BoARd", commands)

    # Even the valid single-characters return False since this function tests for commands.
    assert not is_valid_input("l", commands)
    assert not is_valid_input("f", commands)
    assert not is_valid_input("r", commands)
    assert not is_valid_input("b", commands)
    assert not is_valid_input("", commands) 
    assert not is_valid_input(" ", commands) 
    assert not is_valid_input("q", commands) 
    assert not is_valid_input("e", commands) 
    assert not is_valid_input("a", commands) 
    assert not is_valid_input("v", commands) 
    assert not is_valid_input("L", commands) 
    assert not is_valid_input("F", commands) 
    assert not is_valid_input("R", commands) 
    assert not is_valid_input("B", commands) 
    assert not is_valid_input("W", commands) 

    # Strings with multiple characters
    assert not is_valid_input("ll", commands) 
    assert not is_valid_input("lf", commands) 
    assert not is_valid_input("rf", commands) 
    assert not is_valid_input("Rb", commands) 
    assert not is_valid_input("01", commands) 
    assert not is_valid_input("VA-11 Hall-A", commands) 
    assert not is_valid_input("Anything at all.", commands) 
    assert not is_valid_input("chicken", commands)
    assert not is_valid_input("12345", commands)
    assert not is_valid_input("Spare change", commands) 
    assert not is_valid_input("l" * 10**8, commands) 
    assert not is_valid_input("/ / / / ", commands) 
    assert not is_valid_input(".....", commands) 
    assert not is_valid_input("   ", commands) 


    # Illegal Inputs, (Objects that aren't STR raise an AttributeError)
    mock = mock_func()

    with pytest.raises(AttributeError):
        assert is_valid_input(-1, commands) 
        assert is_valid_input(10**100, commands)
        assert is_valid_input((), commands) 
        assert is_valid_input(frozenset(), commands) 
        assert is_valid_input(mock, commands)   
        assert is_valid_input([], commands)
        assert is_valid_input(set(), commands)
        assert is_valid_input({}, commands)


def test_convert_to_arrows() -> None:
    # Takes in a list of valid moves, then returns their STR arrow equivalent with a maximum of 20 arrows shown.
    conversion = {
        "l": "←",
        "r": "→",
        "f": "↑",
        "b": "↓",
    }

    # Conventional Moves

    # Single-Character Inputs
    assert convert_to_arrows(["l"]) == "←"
    assert convert_to_arrows(["r"]) == "→"
    assert convert_to_arrows(["f"]) == "↑"
    assert convert_to_arrows(["b"]) == "↓"
    
    # Multiple Character Inputs
    assert convert_to_arrows(["l", "l", "l"]) == "←←←"
    assert convert_to_arrows(["r", "l", "b", "f"]) == "→←↓↑"
    assert convert_to_arrows(["f", "r", "l", "f", "r", "l"]) == "↑→←↑→←"
    assert convert_to_arrows(["b", "l", "r", "r"]) == "↓←→→"
    assert convert_to_arrows(["b", "l", "f", "r", "r", "f"]) == "↓←↑→→↑"
    assert convert_to_arrows(["r", "f", "l", "f", "l", "b", "r"]) == "→↑←↑←↓→"
    assert convert_to_arrows(["r", "f", "l", "f", "l", "b", "r"] * 3) == "...↑←↑←↓→→↑←↑←↓→→↑←↑←↓→"

    # Random Assortment of Moves
    mock_con_ar_short = mock_moves_list_gen(10) 
    mock_con_ar_medium = mock_moves_list_gen(21)
    mock_con_ar_long = mock_moves_list_gen(100)
    mock_con_ar_very_long = mock_moves_list_gen(10**4)
    mock_con_ar_very_very_long = mock_moves_list_gen(10**6)

    assert convert_to_arrows(mock_con_ar_short) == ''.join(conversion[mock_con_ar_short[i]] for i in range(10))
    assert convert_to_arrows(mock_con_ar_medium) == '...' + ''.join(
        conversion[mock_con_ar_medium[i]] for i in range(-1,-21,-1)
        )[::-1]
    assert convert_to_arrows(mock_con_ar_long) == '...' + ''.join(
        conversion[mock_con_ar_long[i]] for i in range(-1,-21,-1)
        )[::-1]
    assert convert_to_arrows(mock_con_ar_very_long) == '...' + ''.join(
        conversion[mock_con_ar_very_long[i]] for i in range(-1,-21,-1)
        )[::-1]
    assert convert_to_arrows(mock_con_ar_very_very_long) == '...' + ''.join(
        conversion[mock_con_ar_very_very_long[i]] for i in range(-1,-21,-1)
        )[::-1]


    # Improbable Edge Case: Input Not in Conversion (Raises KeyError)
    with pytest.raises(KeyError):
        assert convert_to_arrows(["x"])
        assert convert_to_arrows(["x", "s", "q"])
        assert convert_to_arrows(["x", "l", "l"])
        assert convert_to_arrows(["l", "x", "l"])
        assert convert_to_arrows(["l"] + ["x"] * 10**8 + ["r"])
        assert convert_to_arrows([""])
        assert convert_to_arrows([])


# MOCK FUNCTION/S FOR TESTING

def mock_moves_list_gen(amount):
# Creates Random Move Sequences
    valid_moves = 'lfrb'
    return [valid_moves[randint(0, 3)] for _ in range(amount)]