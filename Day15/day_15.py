import os
import re
import logging
import time
import datetime

'''
ASSUMPTIONS (from input data):
- more than one beacon cannot be the same minimum distance from a sensor
- a beason and sensor cannot be on the same tile???
'''

file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day_15_input.txt'
padding_size_large = 100
padding_size_medium = 45
padding_char = '-'

beacon_char = 'B'
sensor_char = 'S'
sensor_area_char = '■'

x_horizon_char = '⎯'
y_horizon_char = '|'
origin_char = '✛'

class reading():
    def __init__(self, sensor, beacon, sensor_diameter):
        self.sensor = sensor
        self.beacon = beacon
        self.sensor_diameter = sensor_diameter

class loc():
    def __init__(self,x,y):
        self.x = x
        self.y = y

def read_input(data):
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.INFO)
    
    pairs = []
    for line in data:
        
        start = line.find('=')+1
        end = line.find(',')
        x = int(line[start:end])

        start = line.find('=',start)+1
        end = line.find(':',start)
        y = int(line[start:end])

        sensor=loc(x,y)

        start = line.find('=',start)+1
        end = line.find(',',start)
        x = int(line[start:end])

        start = line.find('=',start)+1
        end = len(line)
        y = int(line[start:end])

        beacon = loc(x,y)

        sensor_diameter = abs(sensor.x-beacon.x)+abs(sensor.y-beacon.y)
        logging.debug(f'{sensor.__dict__=}, {beacon.__dict__=}, {sensor_diameter=}')
        new_pair = reading(sensor,beacon, sensor_diameter)
        pairs.append(new_pair)
    logging.getLogger().setLevel(previous_logging_level)
    return pairs

# Trimming = list of 4 values:
#   index 0: min_y, BOTTOM 
#   index 1: max_y, TOP 
#   index 2: min_x, LEFT 
#   index 3: max_x, RIGHT 


def multi_array_to_str(grid, trm=None):
    '''
    if trm:
        grid_str = '\n'.join([
            ' '.join([
                col
                for col in row[trm[2]:trm[3]]
            ])
            for row in grid[trm[0]:trm[1]]
        ])
        return '\n' + grid_str
    '''
    grid_str = '\n'.join([
        ' '.join([
            col
            for col in row
        ])
        for row in grid
    ])
    
    return '\n' + grid_str

def print_layout():
    meh=1

def day_15_prb_1():
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.DEBUG)
    start_time = time.time()
    logging.info(' day 15, problem 1 '.center(padding_size_large,padding_char))

    with open(input_file,'r') as f:
        data = f.read().splitlines()
        # READ INPUT --------------------------------------------------------------------------
        logging.debug('Reading Input'.center(padding_size_medium,padding_char))
        readings = read_input(data)

    # DISPLAY INITIAL FINDINGS ------------------------------------------------------------
    logging.debug('Mapping Sensors and Beacons'.center(padding_size_medium,padding_char))
    min_y = min([
        r.sensor.y-r.sensor_diameter
        for r in readings
        ])
    max_y = max([
        r.sensor.y+r.sensor_diameter
        for r in readings
        ])
    min_x = min([
        r.sensor.x-r.sensor_diameter
        for r in readings
        ])
    max_x = max([
        r.sensor.x+r.sensor_diameter
        for r in readings
        ])

    logging.debug('GRID DIMENSIONS - with sensor radii')
    logging.debug(f'{min_y=}, {max_y=}')
    logging.debug(f'{min_x=}, {max_x=}')
    # --------------------------------
    # Was using this method to see ALL sensor areas
    # this proved to be inefficient and unwieldy when dealing with LARGE areas
    # Still useful to visualize the smaller example input
    fill_grid = False
    print_grid = True
    trim_grid = False

    if fill_grid:
        trimming = None
        if trim_grid:
            min_y_trimmed = min([
                min(r.sensor.y,r.beacon.y)
                for r in readings
                ])
            max_y_trimmed = max([
                max(r.sensor.y,r.beacon.y)
                for r in readings
                ])
            min_x_trimmed = min([
                min(r.sensor.x,r.beacon.x)
                for r in readings
                ])
            max_x_trimmed = max([
                max(r.sensor.x,r.beacon.x)
                for r in readings
                ])
            
            logging.debug('OLD GRID DIMENSIONS')
            logging.debug(f'{min_y_trimmed=}, {max_y_trimmed=}')
            logging.debug(f'{min_x_trimmed=}, {max_x_trimmed=}') 

            trimming = [
                min_y_trimmed - min_y,  # BOTTOM
                max_y_trimmed - max_y,  # TOP
                min_x_trimmed - min_x,  # LEFT
                max_x_trimmed - max_x  # RIGHT
            ]
            logging.debug(f'{trimming=}')

        # --------------------------------
        # FILL DA GRID
        grid = []
        for y in range(min_y,max_y+1):
            new_row = []
            for x in range(min_x,max_x+1):
                if x == 0:
                    if y == 0:
                        new_row.append(origin_char)
                    else:
                        new_row.append(y_horizon_char)
                elif y == 0:
                    new_row.append(x_horizon_char)
                else:
                    new_row.append('.')
            grid.append(new_row.copy())

        for reading in readings:
            offset_x = reading.sensor.x - min_x
            offset_y = reading.sensor.y - min_y
            grid[offset_y][offset_x] = sensor_char

            offset_x = reading.beacon.x - min_x
            offset_y = reading.beacon.y - min_y
            grid[offset_y][offset_x] = beacon_char
        
        if print_grid:
            grid_str = multi_array_to_str(grid, trimming)
            logging.debug(grid_str)
        
        # SENSOR RADII ------------------------------------------------------------
        logging.debug('Building Radii'.center(padding_size_medium,padding_char))
        for r in readings:
            for i in range(r.sensor.y-r.sensor_diameter, r.sensor.y+r.sensor_diameter+1):
                width = (r.sensor_diameter - abs(i - r.sensor.y))
                # print(f'{i=}, {width=}')

                grid_y = i-min_y
                grid_x = r.sensor.x-min_x
                if grid[grid_y][grid_x] not in [beacon_char, sensor_char]:
                    grid[grid_y][grid_x] = sensor_area_char
                for w in range(width+1):
                    grid_x = r.sensor.x-min_x-w
                    if grid[grid_y][grid_x] not in [beacon_char, sensor_char]:
                        grid[grid_y][grid_x] = sensor_area_char

                    grid_x = r.sensor.x-min_x+w
                    if grid[grid_y][grid_x] not in [beacon_char, sensor_char]:
                        grid[grid_y][grid_x] = sensor_area_char

        if print_grid:
            grid_str = multi_array_to_str(grid, trimming)
            logging.debug(grid_str)

    spots_checked = 0
    view = []
    beacons = [ [r.beacon.x, r.beacon.y] for r in readings ]
    y_check = 2000000
    y = y_check
    for x in range(min_x,max_x+1):
        # logging.debug(f'Checking Column: {x}')
        spotted = False
        for r in readings:
            distance = abs(r.sensor.x-x)+abs(r.sensor.y-y)
            # logging.debug(f'\tDistance from sensor [{r.sensor.x}:{r.sensor.y}]: {distance}<={r.sensor_diameter}')
            if (
                    distance <= r.sensor_diameter
                    and [x,y] not in beacons
                ):
                spotted=True
                break
        if spotted:
            spots_checked += 1
            view.append(sensor_area_char)
        else:
            view.append('.')
    # logging.debug(view)

    # CHECK ROW WHERE BEACON CANNOT BE -------------------------------------
    logging.info(f'FINISHED------- ')
    grid_y_check = y_check - min_y
    logging.info(f'\tChecking y={y_check} for how many spots the beacon CANNOT be')
    # logging.debug(' '.join(grid[grid_y_check]))
    '''
    spots = 0
    for spot in grid[grid_y_check]:
        if spot == sensor_area_char:
            spots += 1
    '''
    logging.info(f'\tANSWER={spots_checked}')
    logging.debug(f'--runtime= {datetime.timedelta(seconds=time.time() - start_time)}')
    logging.getLogger().setLevel(previous_logging_level)


'''
ASSUMPTIONS:
- There is only ONE location unseen by the sensor ranges inside the given restrictions
'''
def day_15_prb_2():
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.DEBUG)
    start_time = time.time()
    logging.info(' day 15, problem 2 '.center(padding_size_large,padding_char))

    with open(input_file,'r') as f:
        data = f.read().splitlines()
        # READ INPUT --------------------------------------------------------------------------
        logging.debug('Reading Input'.center(padding_size_medium,padding_char))
        readings = read_input(data)

    # DISPLAY INITIAL FINDINGS ------------------------------------------------------------
    logging.debug('Checking for Unseen Location(s)'.center(padding_size_medium,padding_char))
        
    min_loc = 0
    max_loc = 4000000

    min_y = min_loc
    max_y = max_loc
    min_x = min_loc
    max_x = max_loc

    logging.debug('GRID DIMENSIONS')
    logging.debug(f'\tY dimensions--{min_y}:{max_y}')
    logging.debug(f'\tX dimensions--{min_x}:{max_x}')
    
    # Taking too long using Problem 1's solution
    # Pivoting to find the "edges" of a sensor's range for each Y-level
    # and seeing if there are any "gaps"
    unchecked_loc = None
    spotted = False
    for y in range(min_y,max_y+1):
        print(f' Checking Row {y-min_y} of {max_y-min_y}', end='\r')

        # Find EDGES of each sensor's range w/in this X --------------------------
        sensor_vision = []
        for r in readings:
            sensor_range_remaining = r.sensor_diameter-abs(r.sensor.y-y)  #abs(r.sensor.x-min_x)+abs(r.sensor.y-y)
            if sensor_range_remaining >= 0: 
                # logging.debug(sensor_range_remaining)
                sensor_sight_min_x = r.sensor.x - sensor_range_remaining
                sensor_sight_max_x = r.sensor.x + sensor_range_remaining

                sensor_vision.append([sensor_sight_min_x,sensor_sight_max_x])
        
        sensor_vision.sort(key=lambda range: range[0])
        # logging.debug(f'{sensor_vision=}')

        current_left_most_checked = min_x
        
        # Now check for any GAPS in the sensor ranges ------------------------------
        for i, sv in enumerate(sensor_vision):
            # logging.debug(f'{sv[0]=}, {current_left_most_checked=}=={(sv[0] > current_left_most_checked)=}')

            # FIRST: see if the left side of the sensor range 
            # matches up with the right edge of the last vision checked (or the perimeter of our view)
            if sv[0] > current_left_most_checked:
                # Since we're assuming there is only ONE unseen location
                # we're just going to assume it's at the edge
                unchecked_loc = loc(current_left_most_checked+1,y) 
                break
            elif sv[1] > current_left_most_checked:
                # Set the current unchecked area as far as the right side of the range we're looking at
                current_left_most_checked = sv[1]
            # ------------------------------------------------------------------------
            # If no unchecked location is found, we need to do some last-minute checks

            # Sensor range is already beyond our scope
            if current_left_most_checked > max_x:
                break 
            # Check if last sensor fails to go beyond our scope: leaving an unchecked sector
            elif i == len(sensor_vision) -1:
                # Again we're assuming that there is only ONE location that is unseen
                unchecked_loc = loc(current_left_most_checked+1,y) 
                break
        if unchecked_loc is not None:
            break

    # logging.debug(view)

    # CHECK ROW WHERE BEACON CANNOT BE -------------------------------------
    logging.info(f'FINISHED------- ')
    logging.debug(f'\tUnchecked spots close by: {unchecked_loc.__dict__}')
    tuning_frequency = unchecked_loc.x * 4000000 + unchecked_loc.y
    logging.info(f'\tANSWER---{tuning_frequency=}')
    logging.debug(f'--runtime= {datetime.timedelta(seconds=time.time() - start_time)}')
    
    logging.getLogger().setLevel(previous_logging_level)

if __name__ == '__main__':
    # Answer is 5256611 spots checked already for beacons
    day_15_prb_1() 

    # Answer is a "tuning frequency" of 13337919186981
    #       the open space was: {'x': 3334479, 'y': 3186981}
    #       Run time was: 0:01:55.166624 (not bad!!!)
    day_15_prb_2() 
