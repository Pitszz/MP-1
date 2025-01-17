import pytest
from random import randint
from game import (
    get_input, 
    get_moves_to_process, 
    is_valid_input, 
    convert_to_arrows
    )

# The functions with no return or yielded values are NOT unit tested.

# INPUT HANDLING TESTS


def test_get_input() -> None:
    # Takes in a STR input from the player, and returns a LIST[STR] of all valid moves from the input.
    controls = set('lfrb')

    # Normal input
    assert get_input("LFRB", controls) == ["l", "f", "r", "b"]
    assert get_input("     R     L      l    k   b ", controls) == ["r", "l", "l", "b"]
    assert get_input("", controls) == []
    assert get_input("llll", controls) == ["l", "l", "l", "l"]
    assert get_input("lfrb" * 10, controls) == ["l", "f", "r", "b"] * 10
    assert get_input("12345678", controls) == []

    # Random words
    assert get_input("          THIS IS HOW YOU DO IT          ", controls) == []
    assert get_input("k k k", controls) == []
    assert get_input("cdrcler", controls) == ["r", "l", "r"]
    assert get_input("SKYDIVER", controls) == ["r"]
    assert get_input("fluffy", controls) == ["f", "l", "f", "f"]
    assert get_input("iwanttodropbuticant", controls) == ["r", "b"]
    assert get_input("mother mary, comes to me", controls) == ["r", "r"]
    assert get_input("thoughtcrime", controls) == ["r"]
    assert get_input("karasu no uta ni akane", controls) == ["r"]
    assert get_input("ich bin ein berliner", controls) == ["b", "b", "r", "l", "r"]
    assert get_input("Embodiment of Scarlet Devil", controls) == ["b", "f", "r", "l", "l"]
    assert get_input("it is what it is", controls) == []
    assert get_input(
        "Hey guys, did you know that in terms of male human and female Pokemon breeding...",
        controls,
    ) == ["r", "f", "l", "f", "l", "b", "r"]
    assert get_input("The Game", controls) == []
    assert get_input("You just lost the game.", controls) == ["l"]
    assert get_input("Life does indeed find a way to f--- you over.", controls) == ["l", "f", "f", "f", "r"]
    assert get_input("But be happy that you're alive today.", controls) == ["b", "b", "r", "l"]

    # EDGE CASES

    # Empty Input
    assert get_input("", controls) == []

    # Really Large Input, (same characters)
    assert get_input("l" * 10**6, controls) == ["l"] * 10**6

    mock_input = mock_moves_list_gen(10**6)
    # Really Large Input, (different characters) 
    assert get_input(''.join(mock_input), controls) == mock_input


def test_get_moves_to_process() -> None:
    previous_moves = [] # mock list

    # This takes in pre-processed input (valid list) and yields the actual moves to be processed given remaining moves
    assert [*get_moves_to_process(["l", "r", "l", "l"], 3, previous_moves)] == ["l", "r", "l"]
    assert [*get_moves_to_process(["f", "r", "b", "l"] * 10, 3, previous_moves)] == ["f", "r", "b"]
    assert [*get_moves_to_process(["l", "r"], 10, previous_moves)] == ["l", "r"]
    assert [*get_moves_to_process(["l", "r", "f", "b"], 0, previous_moves)] == []
    assert [*get_moves_to_process(["l", "r", "f", "b"], 20, previous_moves)] == ["l", "r", "f", "b"]
    assert [*get_moves_to_process(["l", "l", "r", "f", "b"], 5, previous_moves)] == ["l", "l", "r", "f", "b"]
    assert [*get_moves_to_process(["l", "l", "r", "f", "b"], 4, previous_moves)] == ["l", "l", "r", "f"]
    assert [*get_moves_to_process(["l", "r", "f", "b", "l", "f"], 2, previous_moves)] == ["l", "r"]

    #EDGE CASES

    # Negative moves left. Unlikely to happen in-game, but it doesn't hurt to try.
    assert [*get_moves_to_process(["l", "r", "l", "l"], -1, previous_moves)] == []

    # No moves to process. Unlikely to happen in-game as well.
    assert [*get_moves_to_process([], 3, previous_moves)] == []

    # No moves to process & negative moves. (If this happens in-game, the player is a wizard...)
    assert [*get_moves_to_process([], -1, previous_moves)] == []

    # Large Inputs, varying amounts of remaining moves
    assert [*get_moves_to_process(["l"] * 10**6, 0, previous_moves)] == []
    assert [*get_moves_to_process(["l"] * 10**6, 1, previous_moves)] == ["l"]
    assert [*get_moves_to_process(["l"] * 10**6, 100, previous_moves)] == ["l"] * 100
    assert [*get_moves_to_process(["l"] * 10**6, 10**5, previous_moves)] == ["l"] * 10**5
    assert [*get_moves_to_process(["l", "r"] * 10**6, 10**5, previous_moves)] == ["l", "r"] * ((10**5) // 2)
    assert [*get_moves_to_process(["l", "r"] * 10**6, 10, previous_moves)] == ["l", "r"] * 5

    # Using lists comprehension to generate large inputs with random moves.
    # Upper limit with the code is 10**7, it slows down significantly around the 10**6 mark.
    mock_moves_list_1 = mock_moves_list_gen(10**5)
    mock_moves_list_2 = mock_moves_list_gen(10**6) # slows down the test by ~1 second
    mock_moves_list_3 = mock_moves_list_gen(10**7) # slows down the test by ~5 seconds
    # to the tester, don't try 10**8 & above, it'll probably take minutes (i tested & it took about a minute...)

    assert [*get_moves_to_process(mock_moves_list_1, 0, previous_moves)] == []
    assert [*get_moves_to_process(mock_moves_list_2, 0, previous_moves)] == []
    assert [*get_moves_to_process(mock_moves_list_3, 0, previous_moves)] == []
    assert [*get_moves_to_process(mock_moves_list_1, 10, previous_moves)] == mock_moves_list_1[:10]
    assert [*get_moves_to_process(mock_moves_list_2, 10, previous_moves)] == mock_moves_list_2[:10]
    assert [*get_moves_to_process(mock_moves_list_3, 10, previous_moves)] == mock_moves_list_3[:10]
    assert [*get_moves_to_process(mock_moves_list_1, 100, previous_moves)] == mock_moves_list_1[:100]
    assert [*get_moves_to_process(mock_moves_list_2, 100, previous_moves)] == mock_moves_list_2[:100]
    assert [*get_moves_to_process(mock_moves_list_3, 100, previous_moves)] == mock_moves_list_3[:100]
    assert [*get_moves_to_process(mock_moves_list_3, 10**8, previous_moves)] == mock_moves_list_3


def test_is_valid_input() -> None:
    # Checks whether a given input is valid, returns BOOL
    controls = set('lfrb')

    def mock_func():
        def mock_func_in():
            pass

        return mock_func_in

    # Only tests here (if going by the function), are on single letter characters
    assert is_valid_input("l", controls)
    assert is_valid_input("f", controls)
    assert is_valid_input("r", controls)
    assert is_valid_input("b", controls)
    assert not is_valid_input("", controls) 
    assert not is_valid_input(" ", controls) 
    assert not is_valid_input("q", controls) 
    assert not is_valid_input("e", controls) 
    assert not is_valid_input("a", controls) 
    assert not is_valid_input("v", controls) 

    # EDGE CASES: these cases should (for the runtime of the game) never even happen.

    # Strings with multiple characters
    assert not is_valid_input("ll", controls) 
    assert not is_valid_input("lf", controls) 
    assert not is_valid_input("rf", controls) 
    assert not is_valid_input("Rb", controls) 
    assert not is_valid_input("01", controls) 
    assert not is_valid_input("VA-11 Hall-A", controls) 
    assert not is_valid_input("Anything at all.", controls) 
    assert not is_valid_input("Spare change", controls) 
    assert not is_valid_input("l" * 10**8, controls) 
    assert not is_valid_input("/ / / / ", controls) 
    assert not is_valid_input(".....", controls) 
    assert not is_valid_input("   ", controls) 

    # Uppercase characters? 
    assert not is_valid_input("L", controls) 
    assert not is_valid_input("F", controls) 
    assert not is_valid_input("R", controls) 
    assert not is_valid_input("B", controls) 
    assert not is_valid_input("W", controls) 

    #Illegal Inputs
    assert not is_valid_input(-1, controls) 
    assert not is_valid_input(10**100, controls) 
    assert not is_valid_input((), controls) 
    assert not is_valid_input(frozenset(), controls) 

    mock = mock_func()

    # why not? (Passing a Function Object)
    assert not is_valid_input(mock, controls)   

    # Unhashable Illegal Inputs (Raises TypeError)
    with pytest.raises(TypeError):
        assert is_valid_input([], controls)
        assert is_valid_input(set(), controls)
        assert is_valid_input({}, controls)
        

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