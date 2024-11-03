import os
import subprocess
import sys
import time


def clear_screen():
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
        subprocess.run([clear_cmd])


def main(): 
    if len(sys.argv) < 2:
        print('The game requires a filename to start.', file = sys.stderr)
        return 
    with open(sys.argv[1], encoding = 'utf-8-sig') as f:
        clear_screen()
        lengths = {'rows': int(f.readline())}
        move_set = {'moves_left': int(f.readline()), 'your_move': ''}
        start_level = f.read()
        level_info = {'level': start_level.split('\n')[:-1], 'points': 0}
        print('\n'.join(level_info['level']))
        lengths.update({'cols': len(level_info['level'][0])})
        movement(lengths, move_set, level_info)



def movement(lengths, move_set, level_info): # function where the level is modified
    possible_moves = set(('l', 'r', 'f', 'b'))
    print(f'Previous Moves: {move_set['your_move']}')
    print(f'Remaining Moves: {move_set['moves_left']}')
    print(f'Points: {level_info['points']}')
    while move_set['moves_left'] > 0: # other condition is for later
        input_move = input('Enter move/s: ')
        if input_move.lower() in possible_moves:
            move_set['your_move'] += input_move.lower()
            move_set['moves_left'] -= 1
        else:
            print('Invalid Move, clearing...')
            time.sleep(0.4)

        screen(lengths, move_set, level_info) # screen gets updated after
    

# i want to add a somewhat auto-feature where if you type consecutive strings, the game moves on its own
# as long as there are moves left


def screen(lengths, move_set, level_info): # where the screen is modified
    clear_screen()
    dirty_work(lengths, move_set, level_info) 
    print('\n'.join(level_info['level']))
    movement(lengths, move_set, level_info)


def dirty_work(lengths, move_set, level_info): # behind the scenes changes
    return None
