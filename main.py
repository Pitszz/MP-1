import os
import subprocess
import sys
import time


def clear_screen():
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
        subprocess.run([clear_cmd])


def main(): # main() just sets the level up, what the info is, all that jazz
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
            'switch': True, 
            'eggs_in_field': True # switch that determines if there are eggs in field
        }
        lengths.update({'cols': len(level_info['level'][0]) - 1}) # 0 to c - 1
        # calling a start() function would likely be better than calling movement() from the get-go.

        return start(lengths, move_set, level_info)


def start(lengths, move_set, level_info):
    print('\n'.join(level_info['level'])) # shows the level during the beginning.
    # should go to movement() after this. 
    movement(lengths, move_set, level_info)
    clear_screen()
    time.sleep(0.5)
    return game_over(lengths, move_set, level_info)


# break movement function into smaller, unit-testable functions
# explain the movement() function & see how i can split it apart
# movement gets user input
# movement checks if move is valid
# movement also checks the game state end conditions
def movement(lengths, move_set, level_info): # detects user input, what interacts with player
    while move_set['moves_left'] > 0 and level_info['eggs_in_field']:
        print(ui(lengths, move_set, level_info))
        move_set['current_move'] += player_input()
        if movement_check(move_set['current_move']): # redirects to an outside function to test
            return screen(lengths, move_set, level_info)
        else:
            move_set['current_move'] = ''
            print('Invalid Move, clearing...')
            time.sleep(0.4)
            clear_screen()
            print('\n'.join(level_info['level']))


def player_input():
    """
    player_input() is the main function that interacts with the player

    it detects the player's input and returns the input() to the current_move key in move_set
    """
    input_move = input('Enter move/s: ')
    return input_move


def movement_check(current_move): 
    """
    This is a switch that detect whether or not the move is valid or not.

    If the move is valid, it returns True
    If the move is invalid, it returns False

    Might expand this later to encompass chain moves & undo.
    """
    possible_moves = set(('l', 'r', 'f', 'b'))
    if current_move.lower() not in possible_moves:
        return False
    else:
        return True


def ui(lengths, move_set, level_info): 
    # separated the UI from the movement function, why? i have no idea myself.
    previous = f'Previous Moves: {move_set['your_move']}'
    remaining = f'Remaining Moves: {move_set['moves_left']}'
    ui_points = f'Points: {level_info['points']}'
    return '\n'.join((previous, remaining, ui_points))


# i want to add a somewhat auto-feature where if you type consecutive characters, the game moves on its own
# as long as there are moves left

# the screen still flickers, which is pretty bad...
def screen(lengths, move_set, level_info): # where the level is modified
    clear_screen()
    while level_info['switch']: # switch is a variable that tells whether any more eggs can move or not.
        for row_ind in range(lengths['rows'] + 1):
            level_info['level'][row_ind] = [*level_info['level'][row_ind]]
        clear_screen()
        time.sleep(0.5)
        directions(lengths, move_set, level_info) #function where the computations happen
        print('\n'.join(level_info['level']))
    level_info['switch'] = True
    move_set['your_move'] += (move_set['current_move'])
    move_set['current_move'] = ''
    move_set['moves_left'] -= 1
    egg_check(lengths, move_set, level_info)
    movement(lengths, move_set, level_info)


def directions(lengths, move_set, level_info): # we modify level_info['level'] directly
    if move_set['current_move'] == 'l' or move_set['current_move'] == 'f':
        assert move_set['current_move'] == 'l' or move_set['current_move'] == 'f'
        left_up(lengths, move_set, level_info)
    elif move_set['current_move'] == 'r' or move_set['current_move'] == 'b':
        assert move_set['current_move'] == 'r' or move_set['current_move'] == 'b'
        right_down(lengths, move_set, level_info)

    for i in range(lengths['rows'] + 1):
        level_info['level'][i] = ''.join(level_info['level'][i])


def left_up(lengths, move_set, level_info):
    blocked = set(('#', '@', '0'))
    # put every coordinate of egg that moves in moved_eggs
    for row in range(1, lengths['rows']): # not including the outer walls
        if '0' in level_info['level'][row]:
            for col in range(1, lengths['cols']):
                if level_info['level'][row][col] == '0':    
                    if move_set['current_move'] == 'l':
                        if level_info['level'][row][col - 1] not in blocked:
                            move_set['moved_eggs'].append((row, col - 1))
                            level_info['level'][row][col] = '.'
                    if move_set['current_move'] == 'f':
                        if level_info['level'][row - 1][col] not in blocked:
                            move_set['moved_eggs'].append((row - 1, col))
                            level_info['level'][row][col] = '.'
    return return_eggs(lengths, move_set, level_info)   


def right_down(lengths, move_set, level_info):
    blocked = set(('#', '@', '0'))
    # put every coordinate of egg that moves in moved_eggs
    for row in range(lengths['rows'], 0, -1): # not including the outer walls
        if '0' in level_info['level'][row]:
            for col in range(lengths['cols'], 0, -1):
                if level_info['level'][row][col] == '0':    
                    if move_set['current_move'] == 'r':
                        if level_info['level'][row][col + 1] not in blocked:
                            move_set['moved_eggs'].append((row, col + 1))
                            level_info['level'][row][col] = '.'
                    if move_set['current_move'] == 'b':
                        if level_info['level'][row + 1][col] not in blocked:
                            move_set['moved_eggs'].append((row + 1, col))
                            level_info['level'][row][col] = '.'
    return return_eggs(lengths, move_set, level_info)   


def egg_check(lengths, move_set, level_info):
    all_elements_in_map = set()
    for row_ind in range(lengths['rows'] + 1):
            all_elements_in_map.update(*level_info['level'][row_ind])
    if '0' not in all_elements_in_map:
        level_info['eggs_in_field'] = False


def return_eggs(lengths, move_set, level_info):
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


def final_state(lengths, move_set, level_info): # cleaner version of end screen.
    clear_screen()
    print('\n'.join(level_info['level']))
    print(f'Previous Moves: {move_set['your_move']}')
    print(f'You had {move_set['moves_left']} moves left. That\'s pretty slow.')
    print(f'You gained {level_info['points']} points. Good job, I guess.')


main()
