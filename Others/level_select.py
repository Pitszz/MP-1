import os
import subprocess
import sys
import time
import game


def clear_screen():
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
        subprocess.run([clear_cmd], shell = True)


def main():
    clear_screen()
    level_directory = 'levels'
    try:
        levels = os.listdir(level_directory)
        return level_selection(levels)
    except FileNotFoundError:
        print('Error, no Level Directory.', file = sys.stderr)
        return


def read_levels(levels):
    all_levels = []
    print('Here are the available levels: ')
    for level in levels:
        if level.endswith('.in'):
            all_levels.append(custom_name(level))

    return '\n'.join(all_levels)


def custom_name(level):
    # there is a much more efficient way than this, but these levels are just the pre-packaged levels.
    # custom-made levels... where should i place them...
    levels_list = {
        'level0.in': 'Level 1: Base Level', 
        'level1.in': 'Level 2: Topographical Survey', 
        'level2.in': 'Level 3: Rollway to Heaven', 
        'level3.in': 'Level 4: Wing my Way', 
        'level4.in': 'Level 5: The Two Corners', 
        'level5.in': 'Level 6: Bottleneck', 
        'level6.in': 'Level 7: Tunnel-Visioned', 
        'level7.in': 'Level 8: Maze Drawing I', 
        'level8.in': 'Level 9: Chunked Together', 
        'level9.in': 'Level 10: Being for the Benefit of Mr. Egg!'
    }
    if level in levels_list:
        return levels_list[level] 
    else:
        return 'Secret Level ##'


def level_selection(levels):
    possible_levels = set((str(i) for i in range(1, 11)))
    extras = set(('bad', 'lost', 'void'))
    while True:
        print(read_levels(levels))
        choose = input("Please select a level number (1 - 10), or type 'quit' to exit the game: ")
        if choose in possible_levels:
            chosen_level = f'level{int(choose) - 1}.in'
            subprocess.run(['py', 'game.py', 'levels/' + chosen_level])
            time.sleep(1)
            clear_screen()
        else:
            if choose in extras:
                extra_extra(choose)
                break
            elif choose == 'quit':
                quit()

            else:
                print('Not a Valid Level, resetting screen...')
                clear_screen()


def extra_extra(chosen_level):
    if chosen_level == 'bad':
        extra = 'eosd'
    elif chosen_level == 'lost':
        extra = 'lost'
    elif chosen_level == 'void':
        extra = 'cl'
    subprocess.run(['py', 'game.py', 'levels/' + f'level{extra}.in'])


def quit():
    raise StopIteration('Thank you for playing.')


if __name__ == '__main__':
    main()