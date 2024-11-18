import os
import subprocess
import sys
import time

def clear_screen():
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
        subprocess.run([clear_cmd])


def main(): 
    """
    main() is the 'start' function of the whole game.
    it detects if there is a level file or not.
    if there is a level file, the file contents are read and 'loaded' to the script

    Basically, main() is the setup.

    """
    if len(sys.argv) < 2:
        print('No level detected.', file = sys.stderr)
        return 
    with open(sys.argv[1], encoding = 'utf-8-sig') as f:
        clear_screen()
        lengths = {'rows': int(f.readline()) - 1} # 0 to r - 1
        move_set = {
            'moves_left': int(f.readline()), 
            'your_move': '', 
            'current_move': '', 
            'moved_eggs': []
        }
        start_level = f.read()
        level_info = {
            'level': start_level.split('\n')[:-1], 
            'points': 0, 
            'previous_state': [],
            'switch': True, 
            'eggs_in_field': True # switch that determines if there are eggs in field
        }
        lengths.update({'cols': len(level_info['level'][0]) - 1}) # 0 to c - 1

        return start(lengths, move_set, level_info)


def start(lengths, move_set, level_info):
    """
    The start() function, compared to main is just an intermediary function.
    It's job is to pass around the parameters to the display() function.
    it will not return anything from display(), since display() starts the actual game state changes.

    Once display() is done with its calls, start() will finally return a value, the game_over() function.
    
    """
    display(lengths, move_set, level_info)
    clear_screen()
    time.sleep(1.5)
    return game_over(lengths, move_set, level_info)


def display(lengths, move_set, level_info):
    """
    display() is the main user interaction function.

    it shows the UI & detects the user input.

    The while condition checks if there are moves left or there are still eggs in field.
    If True, then the loop will start:
        1. displaying the UI & level on the screen;
        2. asking for the player input; and, 
        3. checking if player input is valid

    If the while condition is False, then display() ends iteration and start() returns the game_over screen
    display() in reality is the display function, while game_state() is the game state function.

    Not unit-testable (I think), it's basically a central function where different, smaller functions are called.

    """
    while end_state_detect(move_set['moves_left'], level_info['eggs_in_field']): # main end_state detection
        print('\n'.join(level_info['level'])) # prints the level before & after calculations
        print(ui(lengths, move_set, level_info)) 
        move_set['current_move'] += player_input()
        if movement_check(move_set['current_move']): # redirects to an outside function to test move validity
            game_state(lengths, move_set, level_info)
        else: # move is invalid or something else entirely (key words: 'reset' & 'undo')
            move_set['current_move'] = '' # move is cleared and the player has to input again. (no moves lost)
            print('Invalid Move, clearing...')
            time.sleep(0.4)
            clear_screen()

# ideally, what should happen is game_state() 
# finishes all of its bullshit & returns its value to display() to print



def player_input(): # unit-testable
    """
    player_input() is the main function that interacts with the player

    it detects the player's input and returns the input() to the current_move key in move_set
    """
    input_move = input('Enter move/s: ')
    return input_move

def movement_check(current_move): # unit-testable
    """
    This is a switch that detect whether or not the move is valid or not.

    If the move is valid, it returns True
    If the move is invalid, it returns False

    Might expand this later to encompass chain moves & undo.
    """
    possible_moves = set(('l', 'r', 'f', 'b'))
    if str(current_move).lower() not in possible_moves:
        return False
    else:
        return True


def ui(lengths, move_set, level_info): # unit-testable, use mock values for values need not to be displayed.
    # separated the UI from the display function, why? i have no idea myself.
    previous = f'Previous Moves: {move_set['your_move']}'
    remaining = f'Remaining Moves: {move_set['moves_left']}'
    ui_points = f'Points: {level_info['points']}'
    return '\n'.join((previous, remaining, ui_points))


def end_state_detect(moves_left, eggs_in_field): # unit-testable
    # returns True if moves_left & eggs_in_field are both True
    if moves_left > 0 and eggs_in_field:
        return True
    else:
        return False


def chain_moves():
    pass


def undo():
    pass


def reset():
    pass

# i want to add a somewhat auto-feature where if you type consecutive characters, the game moves on its own
# as long as there are moves left


# game_state() currently does these:
# detects whether eggs can move or not
# splits each row into lists for appending (done)
# calls the directions function with no return (i think i fixed it to level)
# changes switch
# appends current move to previous moves
# empties current move
# decrements moves left
# calls egg_check
def game_state(lengths, move_set, level_info): # where the level is modified
    while level_info['switch']: # switch is a variable that tells whether any more eggs can move or not.
        level_info['level'] = split_level(lengths['rows'], level_info['level']) # splits the level into a list
        clear_screen()
        time.sleep(0.15)
        if directions(move_set['current_move']): #function where the computations happen
            towards = left_up(lengths['rows'], lengths['cols']) 
        else:
            towards = right_down(lengths['rows'], lengths['cols'])

        level_info['level'] = check_every_row(towards, move_set, level_info)
        print('\n'.join(merge_level(lengths['rows'], level_info['level'])))
        # level_info['level'] = merge_level(lengths['rows'], level_info['level'])

    level_info['switch'] = True
    move_set['your_move'] += (move_set['current_move'])
    move_set['current_move'] = ''
    move_set['moves_left'] -= 1
    egg_check(lengths, move_set, level_info)
    clear_screen()


def split_level(rows, level): # unit-testable (mostly changing 'rows')
    for row_index in range(rows + 1): # since we subtracted 1 from row when placing it in a dictionary
        level[row_index] = list(level[row_index])

    return level


def merge_level(rows, level): # really similar to split_level but instead of splitting, we merge the rows
    for row_index in range(rows + 1): # since we subtracted 1 from row when placing it in a dictionary
        level[row_index] = ''.join(level[row_index])

    return level

# directions function overhaul.
def directions(current_move):
    positive = set(('l', 'f'))
    negative = set(('r', 'b'))
    if current_move in positive:
        return True
    else:
        assert current_move in negative
        return False


def egg_switch(): 
    pass


def egg_check(lengths, move_set, level_info):
    all_elements_in_map = set()
    for row_ind in range(lengths['rows'] + 1):
            all_elements_in_map.update(*level_info['level'][row_ind])
    if '0' not in all_elements_in_map:
        level_info['eggs_in_field'] = False


def left_up(rows, cols):
    to_bottom_right = {
    '_range_row': range(1, rows), 
    '_range_col': range(1, cols),
    'increment': -1,
    'hor': 'l',
    'ver': 'f'
    }

    return to_bottom_right


def right_down(rows, cols):
    to_upper_left = {
    '_range_row': range(rows, 0, -1), 
    '_range_col': range(cols, 0, -1),
    'increment': 1,
    'hor': 'r',
    'ver': 'b'
    }

    return to_upper_left


def check_every_row(towards, move_set, level_info):
    blocked = set(('#', '@', '0'))
    for row in towards['_range_row']:
        if '0' in level_info['level'][row]:
            for col in towards['_range_col']:
                if level_info['level'][row][col] == '0':
                    if move_set['current_move'] == towards['hor']:
                        if level_info['level'][row][col + towards['increment']] not in blocked:
                            move_set['moved_eggs'].append((row, col + towards['increment']))
                            level_info['level'][row][col] = '.'

                    if move_set['current_move'] == towards['ver']:
                        if level_info['level'][row + towards['increment']][col] not in blocked:
                            move_set['moved_eggs'].append((row + towards['increment'], col))
                            level_info['level'][row][col] = '.'

    return return_eggs(move_set, level_info)


def return_eggs(move_set, level_info):
    if not move_set['moved_eggs']: # this means that no eggs are moving anymore
        level_info['switch'] = False
    else:
        for r, c in move_set['moved_eggs']:
            if level_info['level'][r][c] == '.':
                level_info['level'][r][c] = '0'
            elif level_info['level'][r][c] == 'O':
                level_info['level'][r][c] = '@'
                level_info['points'] += 10 + move_set['moves_left']
            elif level_info['level'][r][c] == 'P':
                level_info['points'] -= 5
        move_set['moved_eggs'].clear()

    return level_info['level']


def game_over(lengths, move_set, level_info): # cleaner version of end screen.
    clear_screen()
    print('\n'.join(level_info['level']))
    print(f'Previous Moves: {move_set['your_move']}')
    print(f'You had {move_set['moves_left']} moves left. That\'s pretty slow.')
    print(f'You gained {level_info['points']} points. Good job, I guess.')


if __name__ == '__main__':
    main()
