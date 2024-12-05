import pytest
from random import randint
# using from game import f to avoid using game.f() when asserting (stylistic choice)
from game import (
    move_eggs, 
    all_eggs_blocked, 
    is_inside,
    get_eggs_pos,
    get_range,
    is_end_state, 
    no_eggs_left, 
    get_input, 
    get_moves_to_process, 
    is_valid_input,
    convert_to_arrows,
    )

# The functions with no return values are NOT unit tested.

# CORE LOGIC TESTS

# def test_move_eggs() -> None:
#     # Takes in a GRID, DIRECTION, ROWS, COLS, and MOVES_LEFT -> returns a NEW GRID & SCORE

#     # Moving Right
#     dir = (0, 1)
#     assert move_eggs(dir)

#     # Moving Left
#     dir = (0, -1)
#     assert move_eggs(dir)

#     # Moving Forward
#     dir = (-1, 0)
#     assert move_eggs(dir)

#     # Moving Backward
#     dir = (1, 0)
#     assert move_eggs(dir)


# def test_all_eggs_blocked() -> None:
#     # Takes in a DICT containing the current PUZZLE, ROWS, COLS; and a DIRECTION -> returns a BOOL

#     # Moving Right
#     dir = (0, 1)
#     assert all_eggs_blocked({"puzzle": [], "rows": 0, "cols": 0}, dir)

#     # Moving Left
#     dir = (0, -1)
#     assert all_eggs_blocked({"puzzle": [], "rows": 0, "cols": 0}, dir)

#     # Moving Forward
#     dir = (-1, 0)
#     assert all_eggs_blocked({"puzzle": [], "rows": 0, "cols": 0}, dir)

#     # Moving Backward
#     dir = (1, 0)
#     assert all_eggs_blocked({"puzzle": [], "rows": 0, "cols": 0}, dir)


# def test_is_end_state() -> None:
#     # Takes in a DICT containing the GRID and MOVES_LEFT -> returns a BOOL
#     assert is_end_state({"puzzle": [], "moves_left": 0})


# def test_no_eggs_left() -> None:
#     # Takes in a GRID -> returns a BOOL
#     assert no_eggs_left([])



# INPUT HANDLING TESTS

# def test_get_input() -> None:
#     controls = set('lfrb')

#     # Normal input
#     assert get_input("LFRB", controls) == ["l", "f", "r", "b"]
#     assert get_input("     R     L      l    k   b ", controls) == ["r", "l", "l", "b"]
#     assert get_input("", controls) == []
#     assert get_input("llll", controls) == ["l", "l", "l", "l"]
#     assert get_input("lfrb" * 10, controls) == ["l", "f", "r", "b"] * 10
#     assert get_input("12345678") == []


#     # Random words
#     assert get_input("          THIS IS HOW YOU DO IT          ", controls) == []
#     assert get_input("k k k", controls) == []
#     assert get_input("cdrcler", controls) == ["r", "l", "r"]
#     assert get_input("SKYDIVER", controls) == ["r"]
#     assert get_input("fluffy", controls) == ["f", "l", "f", "f"]
#     assert get_input("iwanttodropbuticant", controls) == ["r", "b"]
#     assert get_input("mother mary, comes to me", controls) == ["r", "r"]
#     assert get_input("thoughtcrime", controls) == ["r"]
#     assert get_input("karasu no uta ni akane", controls) == ["r"]
#     assert get_input("ich bin ein berliner", controls) == ["b", "b", "r", "l", "r"]
#     assert get_input("Embodiment of Scarlet Devil", controls) == ["b", "f", "r", "l", "l"]
#     assert get_input("it is what it is", controls) == []
#     assert get_input(
#         "Hey guys, did you know that in terms of male human and female Pokemon breeding...",
#         controls,
#     ) == ["r", "f", "l", "f", "l", "b", "r"]
#     assert get_input("The Game", controls) == []
#     assert get_input("You just lost the game.", controls) == ["l"]
#     assert get_input("Life does indeed find a way to f--- you over.", controls) == ["l", "f", "f", "f", "r"]
#     assert get_input("But be happy that you're alive today.", controls) == ["b", "b", "r", "l"]


def test_get_moves_to_process() -> None:
    previous_moves = [] # mock list

    # Creates Random Move Sequences
    def mock_moves_list_gen(amount):
        valid_moves = 'lfrb'
        return [valid_moves[randint(0, 3)] for _ in range(amount)]

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
    mock_moves_list_3 = mock_moves_list_gen(10**9) # slows down the test by ~5 seconds
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
    # Checks whether a given input is valid
    controls = set('lfrb')

    def mock_func():
        def mock_func_in():
            pass

        return mock_func_in

    # Only tests here (if going by the function), are on single letter characters
    assert is_valid_input("l", controls) == True
    assert is_valid_input("f", controls) == True
    assert is_valid_input("r", controls) == True
    assert is_valid_input("b", controls) == True
    assert is_valid_input("", controls) == False
    assert is_valid_input(" ", controls) == False
    assert is_valid_input("q", controls) == False
    assert is_valid_input("e", controls) == False
    assert is_valid_input("a", controls) == False
    assert is_valid_input("v", controls) == False

    # EDGE CASES: these cases should (for the runtime of the game) never even happen.

    # Strings with multiple characters
    assert is_valid_input("ll", controls) == False
    assert is_valid_input("lf", controls) == False
    assert is_valid_input("rf", controls) == False
    assert is_valid_input("Rb", controls) == False
    assert is_valid_input("01", controls) == False
    assert is_valid_input("VA-11 Hall-A", controls) == False
    assert is_valid_input("Anything at all.", controls) == False
    assert is_valid_input("Spare change", controls) == False
    assert is_valid_input("l" * 10**8, controls) == False

    # Uppercase characters? 
    assert is_valid_input("L", controls) == False
    assert is_valid_input("F", controls) == False
    assert is_valid_input("R", controls) == False
    assert is_valid_input("B", controls) == False
    assert is_valid_input("W", controls) == False

    # Random and Illegal Inputs
    assert is_valid_input(-1, controls) == False
    assert is_valid_input(10**100, controls) == False
    assert is_valid_input((), controls) == False
    assert is_valid_input(frozenset(), controls) == False
    assert is_valid_input("/ / / / ", controls) == False
    assert is_valid_input(".....", controls) == False
    assert is_valid_input("   ", controls) == False

    mock = mock_func()

    # why not? (Passing a Function Object)
    assert is_valid_input(mock, controls) == False  

    # Unhashable Illegal Inputs
    with pytest.raises(TypeError):
        assert is_valid_input([], controls)
        assert is_valid_input(set(), controls)
        assert is_valid_input({}, controls)
        



# LEVEL

