import game
import pytest

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


def test_moves_split(): 
    assert [*game.moves_split('lll', 100)] == ['l', 'l', 'l']
    assert [*game.moves_split('llkl', 2)] == ['l', 'l']
    assert [*game.moves_split('kkk', 100)] == []
    assert [*game.moves_split('cdrcler', 100)] == ['r', 'l', 'r']
    assert [*game.moves_split('skydiver', 100)] == ['r']
    assert [*game.moves_split(1, 100)] == []
    assert [*game.moves_split('fluffy', 100)] == ['f', 'l', 'f', 'f']
    assert [*game.moves_split('iwanttodropbuticant', 100)] == ['r', 'b']
    assert [*game.moves_split('mother mary, comes to me', 100)] == ['r', 'r']
    assert [*game.moves_split('thoughtcrime', 100)] == ['r']
    assert [*game.moves_split('karasu no uta ni akane', 100)] == ['r']
    assert [*game.moves_split('ich bin ein berliner', 100)] == ['b', 'b', 'r', 'l', 'r']
    assert [*game.moves_split('embodiment of scarlet devil', 100)] == ['b', 'f', 'r', 'l', 'l']
    assert [*game.moves_split('embodiment of scarlet devil', 4)] == ['b', 'f', 'r', 'l']
    assert [*game.moves_split('it is what it is', 100)] == []
    assert [*game.moves_split('hakurei reimu', 0)] == []
    assert [*game.moves_split('Hey guys, did you know that in terms of male human and female Pokemon breeding...', 10)] == ['r', 'f', 'l', 'f', 'l', 'b', 'r']
    assert [*game.moves_split('The Game', 5)] == []
    assert [*game.moves_split('You just lost the game.', 1)] == ['l']


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
