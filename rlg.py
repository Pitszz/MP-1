import subprocess
import os
import sys

from random import randint
from game import clear_screen, merge_level


def main():
    clear_screen()
    print('It cannot be guaranteed that your generated level is solvable.')
    rows = int(input('Please input how many rows (min. 4, max. 35): '))
    if rows > 35:
        rows = 35
    elif rows < 4:
        rows = 4

    cols = int(input('Please input how many columns (min. 4, max. 50): '))
    if cols > 50:
        cols = 50
    elif cols < 4:
        cols = 4

    egg_max = rows * cols // 16
    eggs = int(input(f'Please input how many eggs (Maximum of {egg_max}): '))
    if eggs > egg_max:
        eggs = egg_max
    elif eggs < 1:
        eggs = 1

    return random_base(rows, cols, eggs)


def random_base(rows, cols, eggs):
    level = [[48] * (cols)]
    for i in range(rows - 2):
        new_row = [48]
        for j in range(cols - 2):
            new_row.append(rng())

        level.append(new_row + [48])

    level.append([48] * (cols))
    return random_level(rows, cols, level, eggs)


def rng():
    return randint(0, 63)


def random_level(rows, cols, level, eggs):
    egg_counter = 0
    nest_counter = 0
    egg_nest_coords = set()
    level_made = []
    for ri in range(rows):
        level_row = []
        for ci in range(cols):
            if 0 <= level[ri][ci] <= 43:
                level_row.append('🟩')
            elif 44 <= level[ri][ci] <= 55:
                level_row.append('🧱')
            elif 56 <= level[ri][ci] <= 57:
                level_row.append('🍳')
            else:

                if 58 <= level[ri][ci] <= 60:
                    if nest_counter < eggs:
                        level_row.append('🪹')
                        egg_nest_coords.add((ri, ci))
                        nest_counter += 1
                    else:
                        level_row.append('🟩')

                elif 61 <= level[ri][ci] <= 63: 
                    if egg_counter < eggs:
                        level_row.append('🥚')
                        egg_nest_coords.add((ri, ci))
                        egg_counter += 1
                    else:
                        level_row.append('🟩')

        level_made.append(level_row)

    while egg_counter < eggs:
        coords = (coord_rng(rows, cols))
        if coords not in egg_nest_coords:
            level_made[coords[0]][coords[1]] = '🥚'
            egg_nest_coords.add(coords)
            egg_counter += 1

    while nest_counter < eggs:
        coords = (coord_rng(rows, cols))
        if coords not in egg_nest_coords:
            level_made[coords[0]][coords[1]] = '🪹'
            egg_nest_coords.add(coords)
            nest_counter += 1
     # there are still eggs to be placed
    create_and_play(merge_level(rows, level_made), rows)


def create_and_play(level, rows):  # creates a level to send to game.py
    with open('levels/levelsandbox.in', 'w', encoding = 'utf-8') as levelsb:
        levelsb.write(f'{rows}\n')
        levelsb.write('999\n')
        levelsb.writelines(f'{level}\n')
    # considering the randomness, the player will not be able to retry if level is terrible or not.
    # level is cleared after playing.
    subprocess.run(['py', 'game.py', 'levels/levelsandbox.in'])
    with open('levels/levelsandbox.in', 'w', encoding = 'utf-8') as levelsb:
        levelsb.write('')


    clear_screen()



def coord_rng(rows, cols):
    return (randint(1, rows - 2), randint(1, cols - 2))


if __name__ == '__main__':
    main()