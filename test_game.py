import game
import unittest
def main():
    test_movement_check()
    test_ui()
    test_end_state_detect()
    test_iteration_direction()
    test_egg_check()


def test_movement_check():
    assert game.movement_check('l') == True
    assert game.movement_check('f') == True
    assert game.movement_check('b') == True
    assert game.movement_check('r') == True
    assert game.movement_check('m') == False
    assert game.movement_check(1) == False
    assert game.movement_check(['l']) == False
    assert game.movement_check('00') == False
    assert game.movement_check('ll') == False
    assert game.movement_check('fr') == False
    assert game.movement_check(set()) == False
    assert game.movement_check(' ') == False
    assert game.movement_check(()) == False


def test_ui():
    pass

def test_end_state_detect():
    pass

def test_split_level(): # best way to test this is if there is a row element given in the first place
    pass

def test_iteration_direction(): 
    # a bit iffy to test with random values since movement_check already 
    # i can test if it goes to the correct directional functions also, actually
    pass

def test_increments(): # both horizontal & vertical increments
    pass

def test_direction_check():
    pass

def test_blocked_neighbour():
    pass


def test_egg_check():
    pass


main()