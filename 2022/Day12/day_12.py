import os

import logging
import string

logging.basicConfig(level=logging.INFO)
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day_12_input.txt'
height_map = [] # string.ascii_lowercase
start = []
finish = []
# The longest path will always be the first character
# '○♪x≈ΦαßΓπΣ≡∞⍟☆★'
leading_path_active = '▇'
leading_path_inactive = '▇'
path_char_inactive =  '♘♡♧♤☺♖▽◇△▯▷◴□'
path_char_active ='♞♥♣♠☻♜▼◆▲▮▶◕■' 
# path_characters=path_characters[::-1]

padding_size_large = 100
padding_size = 80
padding_char = '-'

'''
Assumptions: 

'''
def input_to_heightmap(data):
    height_map = [] # string.ascii_lowercase
    start = []
    end = []

    for r,row in enumerate(data):
        new_row = []
        for c, letter in enumerate(row):
            if letter == 'S':
                start = [r,c]
                new_row.append(0)
            elif letter == 'E':
                end = [r,c]
                new_row.append(25)
            else:
                letter_height = string.ascii_lowercase.index(letter)
                new_row.append(letter_height)
        height_map.append(new_row.copy())
    return height_map, start, end

class path():
    def __init__(self, navigation, id=0, active=True,  status=None):
        
        '''
        Reason for not being active: Reached a dead end
        can't traverse b/c:
            1. too steep (up or down)
            2. stumbled onto an existing path (should only be faster or the same distance)
        '''
        self.active = active
        self.navigation = navigation
        self.id = id
        
        # Curerntly unused features --------------------------------------------
        # STATUS: allows us to deal with multiple paths
        '''self.id = id '''
        
        # STATUSES: 
        #   Active: still working
        #   Dead: dead-end OR specifically faster path found 
        #   Inactive: found active path with same step count
        '''self.status = status'''
        # Would be good to record paths of equal step-counts 
        # incase we wanted to randomize paths
        '''self.equal_step_path_id = equal_step_path_id'''

def print_paths(paths,map,end):
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.INFO)
    logging.debug('PRINTING PATHS------')
    
    # ONLY PRINT WHAT'S BEEN TRAVERSED
    only_print_traversed=True
    if only_print_traversed:
        max_row = max([ max([s[0] for s in p.navigation]) for p in paths] + [end[0]] )
        min_row = min([ min([s[0] for s in p.navigation]) for p in paths] + [end[0]] )
        max_col = max([ max([s[1] for s in p.navigation]) for p in paths] + [end[1]] )
        min_col = min([ min([s[1] for s in p.navigation]) for p in paths] + [end[1]] )
        # logging.debug(f'vert dimensions={min_row}:{max_row}')
        # logging.debug(f'horiz dimensions={min_col}:{max_col}')
    else:
        min_row=0
        max_row=len(map)-1
        min_col=0
        max_col=len(map[0])-1

    grid = map.copy()
    grid = [[grid[r][c] for c in range(min_col,max_col+1)] for r in range(min_row,max_row+1)]

    paths.sort(key=lambda x:len(x.navigation))
    for i,p in enumerate(paths):
        grid_row = p.navigation[-1][0] - min_row
        grid_col = p.navigation[-1][1] - min_col
        char_index = p.id%len(path_char_active)
        char = None
        if i==len(paths)-1:
            for step in p.navigation:
                grid[step[0] - min_row][step[1] - min_col] = leading_path_inactive
        if p.active:
            if i==len(paths)-1:
                char = leading_path_active
            else:
                char = path_char_active[char_index]
        else:
            if i==len(paths)-1:
                char = leading_path_inactive
        if char: 
            grid[grid_row][grid_col] = char

    start = paths[0].navigation[0]
    grid[start[0] - min_row][start[1] - min_col] = 'S'
    grid[end[0] - min_row][end[1] - min_col] = 'E'

    grid_str = '\n'.join(
        [
            ' '.join(row)
            for row in grid
        ]
    )
    # print(grid_str)
    logging.getLogger().setLevel(previous_logging_level)
    return grid_str

def day_12_prb_1():
    logging.info(' day 12, problem 1 '.center(padding_size_large,padding_char))
    height_map = [] # string.ascii_lowercase
    found_end = False
    path_to_end = []

    with open(input_file,'r') as f:
        data = f.read().splitlines()
        height_map, start, end =  input_to_heightmap(data)
        logging.debug(f'{start=}, {end=}')
        traversed_map = [
            [ 
                '.' 
                for col in row
            ]
            for row in height_map
        ]
        traversed_map[start[0]][start[1]] = path_char_inactive[0]

        paths = [ path(navigation=[start]) ]
        current_id = paths[0].id

        look = [
            [-1, 0], # North
            [ 0,-1], # East
            [ 1, 0], # South
            [ 0, 1], # West
        ] 

        steps = 0
        while not found_end and len([ p for p in paths if p.active]): 
            # if steps > 20: break
            steps += 1
            # logging.info(f' STEP {steps} '.center(padding_size,padding_char))
            new_paths = []
            paths_str = print_paths(paths, traversed_map,end)
            print(f' STEP {steps} ------------------------------------------------' + '\n' + paths_str + '\n', end='\r')
            for p in paths:
                logging.debug(f'{len(p.navigation)=}, {p.navigation[-1]=}')
                current_pos = p.navigation[-1]
                c_row = current_pos[0]
                c_col = current_pos[1]
                new_directions = []

                for l in look:  
                    l_row = c_row + l[0]
                    l_col = c_col + l[1]
                    
                    if not (
                        l_row < 0 or l_row >= len(traversed_map)
                        or l_col < 0 or l_col >= len(traversed_map[0])
                        or traversed_map[l_row][l_col] != '.'
                    ):
                        height = height_map[l_row][l_col] - height_map[current_pos[0]][current_pos[1]]
                        if height<=1:
                            logging.debug(f'\t{l}=SUCCESS')
                            traversed_map[l_row][l_col] = path_char_inactive[current_id%len(path_char_inactive)]
                            new_directions.append([l_row, l_col])
                            if l_row == end[0] and l_col == end[1]:
                                found_end=False
                                path_to_end = p.navigation.copy() + [new_directions.copy()]
                        else:
                            logging.debug(f'\t{l}=FAILURE')
                    else:
                        logging.debug(f'\t{l}=FAILURE')
                
                logging.debug(f'{new_directions=}')

                if new_directions:
                    for d in new_directions[1:]:
                        new_nav = p.navigation.copy()
                        new_nav.append(d.copy())
                        current_id += 1
                        new_path = path(navigation=new_nav.copy(), id=current_id)
                        new_paths.append(new_path)
                        # traversed_map[d[0]][d[1]] = path_char_inactive[current_id%len(path_char_inactive)]

                    # The first possible path will be a continuation of the current path
                    # We don't want to edit the current path until we copy it's current 
                    # navigation into a new path for the given direction
                    p.navigation += [new_directions[0].copy()]
                    # traversed_map[new_directions[0][0]][new_directions[0][1]] = True

                    logging.debug(f'\t---- adding {len(new_directions)-1} new paths ')
                    logging.debug(f'PATHS: {[p.__dict__ for p in paths]}')
                else:
                    logging.debug(f'\t---- All failures: dactivating path')
                    p.active = False
                logging.debug('-'*10)
            if new_paths:
                paths += new_paths.copy()
            
    print(padding_char*padding_size_large)
    print(f'{len(paths)=}')
    print(f'{path_to_end=}')
    print(f'ANSWER-- {len(path_to_end)-1=}')

def day_12_prb_2():
    logging.info(' day 12, problem 2 '.center(padding_size_large,padding_char))
    height_map = [] # string.ascii_lowercase
    found_end = False
    path_to_end = []

    with open(input_file,'r') as f:
        data = f.read().splitlines()
        height_map, start, end =  input_to_heightmap(data)
        logging.debug(f'{start=}, {end=}')
        traversed_map = [
            [ 
                '.' 
                for col in row
            ]
            for row in height_map
        ]
        paths = []
        current_id = 0
        
        starts = [ 
            [row,col]
            for col in range(len(height_map[0]))
            for row in range(len(height_map))
            if height_map[row][col] == 0
        ]
        for start in starts:
            paths.append(path(navigation=[start], id=current_id))
            traversed_map[start[0]][start[1]] = path_char_inactive[current_id%len(path_char_inactive)]
            current_id += 1

        # paths = [ path(navigation=[start]) ]
        # current_id = paths[0].id
        # traversed_map[start[0]][start[1]] = path_char_inactive[0]

        look = [
            [-1, 0], # North
            [ 0,-1], # East
            [ 1, 0], # South
            [ 0, 1], # West
        ] 

        steps = 0
        while not found_end and len([ p for p in paths if p.active]): 
            # if steps > 20: break
            steps += 1
            # logging.info(f' STEP {steps} '.center(padding_size,padding_char))
            new_paths = []
            paths_str = print_paths(paths, traversed_map,end)
            print(f' STEP {steps} ------------------------------------------------' + '\n' + paths_str + '\n', end='\r')
            for p in paths:
                logging.debug(f'{len(p.navigation)=}, {p.navigation[-1]=}')
                current_pos = p.navigation[-1]
                c_row = current_pos[0]
                c_col = current_pos[1]
                new_directions = []

                for l in look:  
                    l_row = c_row + l[0]
                    l_col = c_col + l[1]
                    
                    if not (
                        l_row < 0 or l_row >= len(traversed_map)
                        or l_col < 0 or l_col >= len(traversed_map[0])
                        or traversed_map[l_row][l_col] != '.'
                    ):
                        height = height_map[l_row][l_col] - height_map[current_pos[0]][current_pos[1]]
                        if height<=1:
                            logging.debug(f'\t{l}=SUCCESS')
                            traversed_map[l_row][l_col] = path_char_inactive[current_id%len(path_char_inactive)]
                            new_directions.append([l_row, l_col])
                            if l_row == end[0] and l_col == end[1]:
                                found_end=False
                                path_to_end = p.navigation.copy() + [new_directions.copy()]
                        else:
                            logging.debug(f'\t{l}=FAILURE')
                    else:
                        logging.debug(f'\t{l}=FAILURE')
                
                logging.debug(f'{new_directions=}')

                if new_directions:
                    for d in new_directions[1:]:
                        new_nav = p.navigation.copy()
                        new_nav.append(d.copy())
                        current_id += 1
                        new_path = path(navigation=new_nav.copy(), id=current_id)
                        new_paths.append(new_path)
                        # traversed_map[d[0]][d[1]] = path_char_inactive[current_id%len(path_char_inactive)]

                    # The first possible path will be a continuation of the current path
                    # We don't want to edit the current path until we copy it's current 
                    # navigation into a new path for the given direction
                    p.navigation += [new_directions[0].copy()]
                    # traversed_map[new_directions[0][0]][new_directions[0][1]] = True

                    logging.debug(f'\t---- adding {len(new_directions)-1} new paths ')
                    logging.debug(f'PATHS: {[p.__dict__ for p in paths]}')
                else:
                    logging.debug(f'\t---- All failures: dactivating path')
                    p.active = False
                logging.debug('-'*10)
            if new_paths:
                paths += new_paths.copy()
    print(f'Number of paths (both active and dead) {len(paths)}')
    print(f'ANSWER-- {len(path_to_end)-1=}')

if __name__ == '__main__':
	# day_12_prb_1() # Answer is 440
	day_12_prb_2() # Answer is 439 (lol)

