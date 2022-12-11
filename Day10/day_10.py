import os
import logging
import re
from math import floor
logging.basicConfig(level=logging.DEBUG)

'''
INCORRECT Answers: 
-15600
-26320
47500

'''
def day_10_prb_1():
    print('day 10, problem 1')

    with open('day_10_input.txt','r') as f:
        data = f.read().splitlines()

        X = 1
        cycle = 0
        signal_strength = 0
        processing_count = 0
        increment = 0
        signal_strength_history = []
        signal_strength_checkins = [20,60,100,140,180,220]

        command_index = 0

        while command_index < len(data):
            #if cycle > 20: break
            cycle += 1
            command = None
            if processing_count > 0:
                processing_count -= 1
                if processing_count == 0:
                    X += increment 
            else:
                
                command = data[command_index].split()
                command_index += 1
                if command[0] == 'addx': 
                    increment = int(command[1])  
                    processing_count = 1
                else: # command[0] == "noop"
                    increment = 0
            
            signal_strength = X * cycle
            if cycle in signal_strength_checkins:
                signal_strength_history.append(signal_strength)
            logging.debug(f'{cycle=}, {X=}, {command=}')	
    print(f'Signal Strengths: {list(zip(signal_strength_checkins,signal_strength_history))}')
    print(f'{sum(signal_strength_history)=}')


def day_10_prb_2():
    print('day 10, problem 2')

    crt_width = 40
    crt_height = 6

    sprite_width = 3
    X = 1
    cycle = 0

    crt = ''
    current_crt_row = '#' # starts with this symbol b/c X=1 for sprite location

    with open('day_10_input.txt','r') as f:
        data = f.read().splitlines()
        command_index = 0
        increment = 0
        processing_count = 0

        while command_index < len(data):
            # if cycle > 70: break
            cycle += 1
            command = None
            if processing_count > 0:
                processing_count -= 1
                if processing_count == 0:
                    X += increment 
            else:
                
                command = data[command_index].split()
                command_index += 1
                if command[0] == 'addx': 
                    increment = int(command[1])  
                    processing_count = 1
                else: # command[0] == "noop"
                    increment = 0
            
            # Determine CRT screen here
            if cycle%crt_width == 0:
                crt += '\n' + current_crt_row
                current_crt_row = ''

            if X < floor(sprite_width/2):
                sprite_left = 0
                sprite_right = sprite_width
            elif X > crt_width-1-floor(sprite_width/2):
                sprite_left = crt_width-sprite_width
                sprite_right = crt_width-1
            else:
                sprite_left = X - floor(sprite_width/2)
                sprite_right = X + floor(sprite_width/2)
            # logging.debug(f'{sprite_left=}, {sprite_right=}')
            # logging.debug(f'{cycle=}, {crt_width=}, {cycle%crt_width-1=}')

            sprite_location = ''.join([
                '#' 
                if (
                    y >= sprite_left 
                    and y <= sprite_right
                )
                else 
                '.'
                for y in range(crt_width)
                ])
            
            new_pixel = sprite_location[cycle%crt_width]
            current_crt_row += new_pixel
            if cycle < 40: 
                logging.debug(f'{cycle=}, {X=}, {command=}')
                logging.debug(f'\t{new_pixel=}')
                logging.debug(f'\t{sprite_location=}')
                logging.debug(f'\t{current_crt_row=}')

                logging.debug('\n' + '-'*20 + '\n')
    
    print(crt)

if __name__ == '__main__':
	# day_10_prb_1()
	day_10_prb_2()


'''
-##..#....#..#.#....#..#.###..####.#.##.
##.#.#....#..#.#....#.#..#..#....#.#.##.
#..#.#....#..#.#....##...###....#..####.
###..#....#..#.#....#.#..#..#..#...#..#.
###..#....#..#.#....#.#..#..#.#....####.
#....####..##..####.#..#.###..####.####.


?LULKBZ?
correct answer= PLULKBZH
'''