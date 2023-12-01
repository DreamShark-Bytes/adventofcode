import os
import re
import logging

logging.basicConfig(level=logging.DEBUG)

'''
ASSUMPTIONS (from input data):
- 
'''

file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day_14_input.txt'
padding_size_large = 100
padding_size = 80
padding_char = '-'

rock_char = '■'
empty_char = '.'
empty_char = '.'
source_char = '+'
moving_sand_char = '~'
stationary_sand_char = 'o'

def read_input(data, sand_source):
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.INFO)
    rock_lines = []
    min_source_x_offset = 0
    max_source_x_offset = 0
    floor_y = 0

    logging.getLogger().setLevel(logging.INFO)
    for i,d in enumerate(data):
        rock_lines.append([])
        for loc in d.split(' -> '):
            new_point = list(map(int,loc.split(',')))
            if new_point[0] - sand_source[0] < min_source_x_offset:
                min_source_x_offset = new_point[0] - sand_source[0]-1
            if new_point[0] - sand_source[0] > max_source_x_offset:
                max_source_x_offset = new_point[0] - sand_source[0]+2
            if new_point[1] - sand_source[1] > floor_y:
                floor_y = new_point[1] - sand_source[1]+3
            rock_lines[i].append(new_point.copy())
        logging.debug(rock_lines[i]) 
        logging.debug('-'*20)

    logging.debug(f'{min_source_x_offset=}, {max_source_x_offset=}, {floor_y=}')
    logging.getLogger().setLevel(previous_logging_level)
    return rock_lines, min_source_x_offset, max_source_x_offset, floor_y

def form_rock_lines(rock_lines, min_source_x_offset, max_source_x_offset, floor_y, sand_source,empty_char,rock_char):
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.INFO)
    abyss_grid = [
        [
            empty_char
            for x in range(0, max_source_x_offset-min_source_x_offset)
        ]
        for y in range(0, floor_y)
    ]
    for lines in rock_lines:
        for point in range(1,len(lines)):
            start_point = lines[point-1]
            end_point = lines[point]
            logging.debug(f'{start_point=}, {end_point=}')
            if start_point[0] != end_point[0]: # Move Horizontal
                increment= (end_point[0]-start_point[0])//abs(end_point[0]-start_point[0])
                logging.debug(f'\tMoving Horizontally')
                for rock in range(start_point[0], end_point[0]+increment, increment):
                    rock_x = rock-sand_source[0]-min_source_x_offset
                    rock_y = start_point[1]-sand_source[1]
                    logging.debug(f'\t\tx{rock},y{start_point[1]}==x{rock_x},y{rock_y}')
                    abyss_grid[rock_y][rock_x] = rock_char

            else: # Move Vertical
                increment= (end_point[1]-start_point[1])//abs(end_point[1]-start_point[1])
                logging.debug(f'\tMoving Vertically')
                for rock in range(start_point[1], end_point[1]+increment, increment):
                    rock_x = start_point[0]-sand_source[0]-min_source_x_offset
                    rock_y = rock-sand_source[1]
                    logging.debug(f'\t\tx{rock},y{start_point[1]}==x{rock_x},y{rock_y}')
                    abyss_grid[rock_y][rock_x] = rock_char
    logging.getLogger().setLevel(previous_logging_level)
    return abyss_grid

def day_14_prb_1():
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.INFO)
    logging.info(' day 14, problem 1 '.center(padding_size_large,padding_char))

    #  [x,y] = [right, down]
    #       y=0 is the highest location

    #              [x,y]
    sand_source = [500,0]

    rock_lines = []
    abyss_grid = []
    min_source_x_offset = 0
    max_source_x_offset = 0
    floor_y = 0

    with open(input_file,'r') as f:
        data = f.read().splitlines()
        # READ INPUT --------------------------------------------------------------------------
        rock_lines, min_source_x_offset, max_source_x_offset, floor_y = read_input(data, sand_source)

        # FORM ROCK LINES --------------------------------------------------------------------

        abyss_grid = form_rock_lines(rock_lines, min_source_x_offset, max_source_x_offset, floor_y, sand_source, empty_char,rock_char)
        abyss_grid[0][-min_source_x_offset] = source_char

        # LET THE SPICE FLOW --------------------------------------------------------------------
        logging.getLogger().setLevel(logging.DEBUG)
        source_sand = [0,-min_source_x_offset] # NOTE: y,x
        current_sand = source_sand.copy()
        current_sand_path = [current_sand.copy()]
        
        resting_sand = 0

        loops = 0
        while current_sand[0] < floor_y-1:
            loops += 1
            # if loops >100: break
            down_directions = [
                 0,    # straight down
                -1,    # Down-LEFT
                 1     # Down-RIGHT
                ]
            moved = False
            for d in down_directions:
                open_space_check = abyss_grid[current_sand[0]+1][current_sand[1]+d]
                if open_space_check != rock_char and open_space_check != stationary_sand_char:
                    current_sand=[current_sand[0]+1,current_sand[1]+d]
                    moved = True
                    break
            if not moved:
                abyss_grid[current_sand[0]][current_sand[1]] = stationary_sand_char
                resting_sand += 1
                current_sand = source_sand.copy()
                current_sand_path = []
                logging.debug(f'Sand location on grid: {current_sand}')
                logging.debug('\n' + '\n'.join([ ' '.join(row) for row in abyss_grid]))
            else:
                current_sand_path.append(current_sand.copy())

    grid_w_moving_sand = '\n'.join([
            ' '.join([
            moving_sand_char
            if [row_i,col_i] in current_sand_path
            else abyss_grid[row_i][col_i]
            for col_i in range(len(abyss_grid[0]))
        ])
        for row_i in range(len(abyss_grid))
    ])
    logging.info('\n' + grid_w_moving_sand)
    logging.info(f'FINISHED-- {resting_sand=}')
    logging.getLogger().setLevel(previous_logging_level)

# Keep track of Offests outside of here, wtherwise we'd have to do a lot of tedious calculations
def print_grid(sand_source,floor_y, min_source_x_offset, max_source_x_offset, rocks, floor_exists, stationary_sand=[]):
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.DEBUG)
    # NOTE: Grid changes the X and Y positions of the 
    grid = [
        [
            empty_char
            for x in range(0, max_source_x_offset-min_source_x_offset)
        ]
        for y in range(0, floor_y)
    ]
    for rock in rocks:
        x = rock[0]-sand_source[0]-min_source_x_offset
        y = rock[1]-sand_source[1]-floor_y
        grid[y][x] = rock_char
    
    if floor_exists:
        for col in range(max_source_x_offset-min_source_x_offset):
            grid[floor_y-1][col] = rock_char
    
    grid[0][-min_source_x_offset] = source_char
    
    for grain_of_sand in stationary_sand:
        x = grain_of_sand[0]-sand_source[0]-min_source_x_offset
        y = grain_of_sand[1]-sand_source[1]-floor_y
        grid[y][x] = stationary_sand_char

    
    grid_str = '\n'.join([
        ' '.join([
            col
            for col in row
        ])
        for row in grid
    ])
    logging.debug('\n' + grid_str)
    logging.getLogger().setLevel(previous_logging_level)

# Created this code to find a solution for EITHER part 1 or part 2
#   part 1: if any sand falls into the abyss: floor_exists=False
#   part 2: when sand piles up enough to cover the sand_source: floor_exists=True
def day_14_prb_2():
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info(' day 14, problem 2 '.center(padding_size_large,padding_char))

    #  [x,y] = [right, down]
    #       y=0 is the highest location

    #              [x,y]
    sand_source = [500,0]

    floor_exists = True
    floor_y = 0

    rock_lines = []
    min_source_x_offset = 0
    max_source_x_offset = 0
    
    with open(input_file,'r') as f:
        data = f.read().splitlines()
        # READ INPUT --------------------------------------------------------------------------
        rock_lines, min_source_x_offset, max_source_x_offset, floor_y = read_input(data, sand_source)
        logging.debug(f'{floor_y=}')

        # FORM ROCK LINES --------------------------------------------------------------------
        rocks = []
        logging.getLogger().setLevel(logging.DEBUG)
        for lines in rock_lines:
            for point in range(1,len(lines)):
                start_point = lines[point-1]
                end_point = lines[point]
                logging.debug(f'{start_point=}, {end_point=}')
                if start_point[0] != end_point[0]: # Move Horizontal
                    increment= (end_point[0]-start_point[0])//abs(end_point[0]-start_point[0])
                    logging.debug(f'\tMoving Horizontally')
                    for rock_x in range(start_point[0], end_point[0]+increment, increment):
                        rock = [rock_x,start_point[1]]
                        if rock not in rocks: rocks.append(rock)
                else: # Move Vertical
                    increment= (end_point[1]-start_point[1])//abs(end_point[1]-start_point[1])
                    logging.debug(f'\tMoving Vertically')
                    for rock_y in range(start_point[1], end_point[1]+increment, increment):
                        rock = [start_point[0],rock_y]
                        if rock not in rocks: rocks.append(rock)
        logging.debug(rocks)
        logging.debug(f'{len(rocks)=}')
        print_grid(sand_source, floor_y,min_source_x_offset,max_source_x_offset, rocks, floor_exists)

        # LET THE SPICE FLOW --------------------------------------------------------------------
        stationary_sand = []

        logging.getLogger().setLevel(logging.INFO)
        current_sand = sand_source.copy()
        current_sand_path = [current_sand.copy()]

        loops = 0
        while (len(stationary_sand) == 0 or stationary_sand[-1] != sand_source) and current_sand[1] < floor_y-1:
            loops += 1
            # if loops >300: break
            down_directions = [
                 0,    # straight down
                -1,    # Down-LEFT
                 1     # Down-RIGHT
                ]
            moved = False
            for d in down_directions:
                
                # ----------- match source: [x,y]
                next_move = [current_sand[0]+d,current_sand[1]+1] 
                next_move_X_offset = next_move[0] - sand_source[0]

                if next_move_X_offset < min_source_x_offset:
                    min_source_x_offset = next_move_X_offset
                elif next_move_X_offset > max_source_x_offset:
                    max_source_x_offset = next_move_X_offset 
                logging.debug(f'Attempting to move: FROM: {current_sand}, TO:{next_move}')

                if next_move in rocks:
                    logging.debug('\tCannot move: ROCK in way')
                elif next_move in stationary_sand:
                    logging.debug('\tCannot move: SAND in way')
                elif floor_exists and next_move[1] == floor_y-1:
                    logging.debug('\tCannot move: FLOOR in way')
                elif not floor_exists and next_move[1] == floor_y:
                    logging.debug('\tCannot move: INTO THE ABYSS')
                else:
                    current_sand=next_move.copy()
                    current_sand_path.append(current_sand.copy())
                    moved = True
                    logging.debug('\tMOVED')
                    break
            if not moved:
                logging.debug(f'Sand location on grid: {current_sand}')
                stationary_sand.append(current_sand.copy())

                print_grid(sand_source, floor_y,min_source_x_offset,max_source_x_offset, rocks, floor_exists, stationary_sand)
                current_sand = sand_source.copy()
                current_sand_path = []
            else:
                current_sand_path.append(current_sand.copy())

    logging.info(f'FINISHED-- {len(stationary_sand)=}')
    logging.getLogger().setLevel(previous_logging_level)

if __name__ == '__main__':
    # day_14_prb_1() # Answser is 1513 resting grains of sand by the time one falls into the abyss.
    day_14_prb_2() # Answer is 22646 resting grains of sand before it touches the sand's source