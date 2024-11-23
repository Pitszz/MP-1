import os
import subprocess
import sys
import time
import copy



def clear_screen():
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
        subprocess.run([clear_cmd], shell = True)


def main(): 
    """
    main() is the 'start' function of a level.
    it detects if there is a level file or not.
    if there is a level file, the file contents are read and 'loaded' to the script

    Basically, main() is the setup.

    """
    if len(sys.argv) < 2:
        print('No level detected.', file = sys.stderr)
        return 
    with open(sys.argv[-1], encoding = 'utf-8') as f:
        clear_screen()
        lengths = {'rows': int(f.readline())} 
        # More about user interaction with the game.
        move_set = {
            'moves_left': int(f.readline()),
            'your_move': '', 
            'current_move': '',
            'undos_left': 3, 
            'moved_eggs': []
        }
        # More about game state & display.
        level_info = {
            'level': ''.join([*f.read()]).split('\n')[:-1], 
            'points': 0, 
            'points_gained': [0], # tracks how many points were gained or lost per move, starts with a 0 for easier calculations
            'previous_state': [],
            'egg_switch': True, 
        }
        lengths.update({'cols': len(level_info['level'][0])})
        starting_info = {
            'start_move_set': {
                'moves_left': move_set['moves_left'],
                'your_move': '', 
                'current_move': '',
                'undos_left': 3, 
                'moved_eggs': []
            },
            'start_level_info': {
                'level': level_info['level'].copy(), 
                'points': 0, 
                'points_gained': [0],
                'previous_state': [],
                'egg_switch': True, 
            }
        }

        return start(lengths, starting_info, move_set, level_info)


def start(lengths, starting_info, move_set, level_info):
    """
    The start() function, compared to main is just an intermediary function.
    It's job is to pass around the parameters to the display() function.
    it will not return anything from display(), since display() starts the actual game state changes.

    Once display() is done with its calls, start() will finally return a value, the game_over() function.
    
    """
    display(lengths, starting_info, move_set, level_info)
    clear_screen()
    return game_over(lengths, starting_info, move_set, level_info)


def display(lengths, starting_info, move_set, level_info):
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
    while end_state_detect(lengths['rows'], move_set['moves_left'], level_info['level']): # main end_state detection
    # it does feel a bit weird that end_state detection is appended to display() & not game_state()
        print('\n'.join(level_info['level'])) # prints the level before & after calculations
        print(ui(lengths, move_set, level_info))
        move_set['current_move'] += player_input()
        if special_move(move_set['current_move']): # detects first if the player gives a special input
            special_moves_list(lengths, starting_info, move_set, level_info)
        else: # if not, it's likely a valid move
            chain_moves = [*moves_split(move_set['current_move'], move_set['moves_left'])]
            if chain_moves:
                for move in chain_moves: # still a bit spaghetti... (fix this later)
                    temp_prev_level = level_info['level'].copy() # holds previous level state temporarily
                    level_info['previous_state'].append(iter(temp_prev_level))
                    # sending an 
                    move_set['current_move'] = move
                    if eggs_in_field(lengths['rows'], level_info['level']):
                        game_state(lengths, starting_info, move_set, level_info)
            else: # move is invalid
                move_set['current_move'] = '' # current_move is cleared and the player has to input again. (no moves lost)
                print('No valid moves, clearing...')
                time.sleep(0.4)
                clear_screen()


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

    """
    possible_moves = set(('l', 'r', 'f', 'b'))
    if str(current_move).lower() not in possible_moves:
        return False
    else:
        return True

def moves_split(current_move, moves_left):
    """
    The chain moves function.
    The player can input a string sequence of characters & the only moves that will be accepted by
    the game are valid moves.

    """
    remaining_moves = moves_left
    all_moves = list(str(current_move))
    for move in all_moves:
        if movement_check(str(move)) and remaining_moves > 0:
            yield move
            remaining_moves -= 1



def ui(lengths, move_set, level_info): # unit-testable, use mock values for values need not to be displayed.
    """
    Dislays the UI of the player.
    """
    previous = f'Previous Moves: {move_set['your_move']}'
    remaining = f'Remaining Moves: {move_set['moves_left']}'
    undo_remaining = f'Undos Left: {move_set['undos_left']}'
    ui_points = f'Points: {level_info['points']}'
    return '\n'.join((previous, remaining, undo_remaining, ui_points))


def end_state_detect(rows, moves_left, level): # unit-testable
    """
    End State Detection, returns True if there are no moves left & no more eggs in field
    """
    if moves_left > 0 and eggs_in_field(rows, level):
        return True
    else:
        return False

def eggs_in_field(rows, level):
    """
    One of the end state detectors, senses if there are no more eggs in field
    """
    all_elements_in_map = set()
    for row_ind in range(rows):
            all_elements_in_map.update(*level[row_ind])
    if '🥚' in all_elements_in_map:
        return True

    else:
        return False


def special_move(current_move):
    possible_moves = set(('reset', 'undo', 'quit', 'exit'))
    if current_move in possible_moves:
        return True
    else:
        return False


def special_moves_list(lengths, starting_info, move_set, level_info):
    if move_set['current_move'].lower() == 'quit':
        return quit_game(move_set)
    elif move_set['current_move'].lower() == 'reset':
        reset_level(lengths, starting_info, move_set, level_info)
    elif move_set['current_move'].lower() == 'exit':
        return exit_level(lengths, starting_info, move_set, level_info)
    elif move_set['current_move'].lower() == 'undo':
        undo(lengths, move_set, level_info)


def quit_game(move_set):
    while True:
        exit_input = input('Are you sure you want to quit the game? [Y/N]: ')
        if exit_input.upper() == 'Y':
            raise StopIteration('Thank you for playing.')
        elif exit_input.upper() == 'N':
            move_set['current_move'] = ''
            print('The game continues.')
            time.sleep(0.5)
            clear_screen()
            break
            
        else:
            print('Haha, very funny.')
            continue

def reset_level(lengths, starting_info, move_set, level_info):
    print('Resetting level...')
    temp_move_set = copy.deepcopy(starting_info['start_move_set'])
    temp_start_level = copy.deepcopy(starting_info['start_level_info'])
    # temporary copy of the dicts in starting_info to avoid infecting the dicts in starting_info due to mutable data types
    time.sleep(0.5)
    clear_screen()
    move_set.update(temp_move_set)
    level_info.update(temp_start_level)


    


def exit_level(lengths, starting_info, move_set, level_info):
    while True:
        go_to_level_screen = input('Go back to level selection screen? [Y/N]: ')
        if go_to_level_screen.upper() == 'Y':
            return level_screen()
        elif go_to_level_screen.upper() == 'N':
            move_set['current_move'] = ''
            print('The game continues.')
            time.sleep(0.5)
            clear_screen()
            return move_set
        else:
            print('Haha, very funny.')
            continue


def undo(lengths, move_set, level_info):
    """
    The player only has a limited amount of undos & is dependent on there being a previous_state to undo to, 
    and remaining undos left. 
    """
    move_set['current_move'] = ''
    if move_set['undos_left'] and level_info['previous_state']:
        clear_screen()
        move_set['undos_left'] -= 1
        move_set['moves_left'] += 1
        move_set['your_move'] = move_set['your_move'][:-1]
        level_info['level'] = [*level_info['previous_state'][-1]]
        level_info['points'] -= level_info['points_gained'][-1]
        level_info['points_gained'].pop()
        level_info['previous_state'].pop()
    else:
        if not level_info['previous_state']:
            print('You can\'t go back to a previous state.')
        if not move_set['undos_left']:
            print('No more undos left!')

        time.sleep(0.5)
        clear_screen()


    # go to previous state
    # append moves_left by one
    # removing previous move from moves_left


        


def game_state(lengths, starting_info, move_set, level_info): # Not unit-testable, another main loop
    """
    game_state() is the main function that executes the game state changes.

    It does:
    1. Detects whether any eggs can move.
    2. Modifies the level & shows the progress.
    3. Updates the game state.

    """
    while level_info['egg_switch']: # switch is a variable that tells whether any more eggs can move or not.
        level_info['level'] = split_level(lengths['rows'], level_info['level']) # splits the level into a list
        clear_screen()
        if iteration_direction(move_set['current_move']):
            towards = left_up(lengths['rows'], lengths['cols']) 
        else:
            towards = right_down(lengths['rows'], lengths['cols'])

        level_info['level'] = row_egg_check(towards, move_set, level_info)
        print(merge_level(lengths['rows'], level_info['level']))
        time.sleep(0.25)
        clear_screen()

    

    return updated_game_states(level_info, move_set)


def updated_game_states(level_info, move_set): # unit-testable
    """
    Updates the visible game states like moves left & previous moves.
    Empties current_move, so new single letter moves can be added.
    Also turns on egg_switch allowing game_state() to function again once it is called after display().
    """
    level_info['egg_switch'] = True
    level_info['points_gained'].append(level_info['points'] - sum(level_info['points_gained']))
    move_set['your_move'] += (move_set['current_move'].lower())
    move_set['current_move'] = ''
    move_set['moves_left'] -= 1

    return level_info, move_set


def split_level(rows, level): # unit-testable (mostly changing 'rows')
    """
    Turns each row of the level grid into lists for better append
    """
    for row_index in range(rows): # since we subtracted 1 from row when placing it in a dictionary
        level[row_index] = list(level[row_index])

    return level


def merge_level(rows, level): # really similar to split_level but instead of splitting, we merge the rows
    for row_index in range(rows): # since we subtracted 1 from row when placing it in a dictionary
        level[row_index] = ''.join(level[row_index])


    return '\n'.join(level)

# directions function overhaul.
def iteration_direction(current_move):
    positive = set(('l', 'f'))
    negative = set(('r', 'b'))
    if current_move.lower() in positive:
        return True
    else:
        assert current_move.lower() in negative
        return False


def return_eggs(move_set, level_info):
    if not move_set['moved_eggs']: # this means that no eggs are moving anymore
        level_info['egg_switch'] = False
    else:
        for r, c in move_set['moved_eggs']:
            if level_info['level'][r][c] == '🟩':
                level_info['level'][r][c] = '🥚'
            elif level_info['level'][r][c] == '🪹':
                level_info['level'][r][c] = '🪺'
                level_info['points'] += 10 + move_set['moves_left']
            elif level_info['level'][r][c] in set(('🍳', ' ')):
                level_info['points'] -= 5
        move_set['moved_eggs'].clear()

    return level_info['level']


def left_up(rows, cols):
    to_bottom_right = {
    '_range_row': range(rows), 
    '_range_col': range(cols),
    'increment': -1,
    'hor': 'l',
    'ver': 'f'
    }

    return to_bottom_right


def right_down(rows, cols):
    to_upper_left = {
    '_range_row': range(rows - 1, -1, -1), 
    '_range_col': range(cols - 1, -1, -1),
    'increment': 1,
    'hor': 'r',
    'ver': 'b'
    }

    return to_upper_left


def row_egg_check(towards, move_set, level_info):
    """
    Checks each row if there is an egg.
    If there is, check precisely (just a term for by column)
    If there is not, skip the row & keep iterating.
    """
    for row in towards['_range_row']:
        if '🥚' in level_info['level'][row]:
            level_info['level'][row] = precise_egg_check(towards, move_set, level_info['level'], row)
        else:
            continue

    return return_eggs(move_set, level_info)

def precise_egg_check(towards, move_set, level, row):
    """
    Checks each column of a row to see if there is an egg.
    If there is, check if the move is horizontal or vertical # another function.
    take its coordinates & append to moved_eggs. # another function might be better for that.

    """
    for col in towards['_range_col']:
        if level[row][col] == '🥚':
            coords = (row, col)
            level[row][col] = horizo_vertical(towards, move_set, level, coords)

    return level[row]


def horizo_vertical(towards, move_set, level, coords):
    row, col = [*coords]
    if direction_check(move_set['current_move'], towards):
        return horizontal_increment(towards, move_set, level, coords)
    else:
        return vertical_increment(towards, move_set, level, coords)


def horizontal_increment(towards, move_set, level, coords):
    row, col = [*coords]
    point = level[row][col]
    neighbour = (row, col + towards['increment'])
    if blocked_neighbour(neighbour, level):
        move_set['moved_eggs'].append(neighbour)
        point = '🟩'

    return point


def vertical_increment(towards, move_set, level, coords):
    row, col = [*coords]
    point = level[row][col]
    neighbour = (row + towards['increment'], col)
    if blocked_neighbour(neighbour, level):
        move_set['moved_eggs'].append(neighbour)
        point = '🟩'

    return point


def blocked_neighbour(neighbour, level):
    row, col = [*neighbour]
    blocked = set(('🧱', '🪺', '🥚'))
    if level[row][col] not in blocked:
        return True
    else:
        return False


def direction_check(current_move, towards):
    if current_move.lower() == towards['hor']:
        return True

    else:
        assert current_move.lower() == towards['ver']
        return False


def game_over(lengths, starting_info, move_set, level_info): # cleaner version of end screen.
    clear_screen()
    print('\n'.join(level_info['level']))
    print(f'Previous Moves: {move_set['your_move']}')
    print(f'You had {move_set['moves_left']} move(s) left.')
    print(f'You gained {level_info['points']} point(s).')


if __name__ == '__main__':
    main()
