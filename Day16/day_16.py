import os
import re
import logging
import time
import datetime
import json

'''
ASSUMPTIONS (from input data):
- Valves have unique names
- tunnels alway go both ways (this is visible in both the example and provided inputs)
- home base is always valve 'AA', which has no pressure
'''

file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day_16_input.txt'
padding_size_large = 100
padding_size_medium = 45
padding_char = '-'

class valve():
    def __init__(self, name, flow_rate, leads_to=None):
        self.name = name
        self.flow_rate = flow_rate
        if leads_to is None:
            leads_to = []
        self.leads_to = leads_to

def read_input(data):
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.INFO)
    
    valves = {}
    for line in data:
        l = line.split(' ')
        valve_name = l[1]
        flow_rate = int(l[4][len('rate='):l[4].find(':')])
        v = valve(valve_name, flow_rate)
        leading_to_start = 9
        for leads in l[leading_to_start:]:
            v.leads_to.append(leads.strip(","))
        valves[valve_name]=v
        logging.debug(f'{valve_name}::{v.__dict__=}')
        
    logging.getLogger().setLevel(previous_logging_level)
    return valves

# wanted to verify all tunnels are two way so I can measure
def verify_tunnels_are_two_way(valves):
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.INFO)
    two_way_tunnels = True
    for k,v in valves.items():
        name = k
        self_in_children = True
        for other_valve in v.leads_to:
            if name not in  valves[other_valve].leads_to:
                self_in_children==False
                break
        logging.debug(f'{name=} :: {self_in_children=}')
        if not self_in_children:
            two_way_tunnels == False
    logging.getLogger().setLevel(previous_logging_level)
    return two_way_tunnels

def find_valve_distances(valves):
    # NOTE: can improve speed by adding found paths from one valve to another
    valve_distances = {}
    for parent_valve_name,parent_valve_details in valves.items():
        logging.debug(f'Shortest Steps for {parent_valve_name}')
        steps = 0
        valve_distances[parent_valve_name] = {}
        logging.debug(f'\tfound SELF -- {steps=}' + '-'*20)
        valves_exploring = parent_valve_details.leads_to

        while len(valve_distances[parent_valve_name].keys()) < len(valves.keys())-1:
            steps += 1
            if steps >= len(valves.keys()): raise Exception(f'ERROR: ran out of steps searching for best paths from: {parent_valve_name}')
            next_valves_to_explore = []
            logging.debug(f'\tSTEP {steps}' + '-'*20)
            logging.debug(f'\tNow checking out these: {valves_exploring}')
            # Take the "leads_to" values of the found
            for new_v in valves_exploring:
                if new_v not in valve_distances[parent_valve_name].keys() and new_v != parent_valve_name:
                    valve_distances[parent_valve_name][new_v] = steps
                    logging.debug(f'\tfound {new_v} -- which leads to: {valves[new_v].leads_to}')
                    new_leads = []
                    for visit_next in valves[new_v].leads_to:
                        
                        if visit_next not in valve_distances[parent_valve_name].keys() and visit_next not in new_leads:
                            new_leads.append(visit_next)

                    logging.debug(f'\t\tNext time look at: {new_leads}')
                    next_valves_to_explore += new_leads.copy()
            valves_exploring = next_valves_to_explore.copy()
    return valve_distances

def valve_permutations(time_left, current_loc_name, valves_left_to_turn_on, valve_distances, pressure_release_history=[]):
    # pressure_release_history -- List
    #   each item is another list: [ valve_name, pressure_released]

    # valves_left_to_turn_on -- List
    #   each item is another list: [ valve_name, flow_rate]
    
    most_pressure_released = 0
    temp_pressure_release_history = pressure_release_history.copy()
    new_pressure_release_history = None
    total_valves = len(pressure_release_history)+len(valves_left_to_turn_on)
    depth = total_valves-len(valves_left_to_turn_on)

    for i,check_valve in enumerate(valves_left_to_turn_on):
        
        check_valve_name = check_valve[0]
        check_valve_flow_rate = check_valve[1]
        if len(valves_left_to_turn_on) == 0: continue

        time_to_walk_and_turn_on = valve_distances[current_loc_name][check_valve_name]+1

        new_time_left = time_left-time_to_walk_and_turn_on # -1 to turn on the valve

        if new_time_left <= 0:
            continue
        else:
            pressure_released = new_time_left * check_valve_flow_rate
            logging.debug('|\t'*(depth) + f'Moving to: {check_valve} --- {time_left}-{time_to_walk_and_turn_on}={new_time_left}, p:{pressure_released}')
            temp_valves_left_to_turn_on = valves_left_to_turn_on.copy()
            del temp_valves_left_to_turn_on[i]

            temp_pressure_release_history = valve_permutations(
                new_time_left, 
                check_valve_name, 
                temp_valves_left_to_turn_on, 
                valve_distances, 
                pressure_release_history + [[check_valve_name, pressure_released]]
                )
            if temp_pressure_release_history:
                temp_pressure_released = sum([tmpro[1] for tmpro in temp_pressure_release_history])
                logging.debug('|\t'*(depth) + f'**END FOUND: total={temp_pressure_released}:{temp_pressure_release_history}')
                if temp_pressure_released > most_pressure_released:
                    most_pressure_released = temp_pressure_released
                    new_pressure_release_history = temp_pressure_release_history.copy()

    if valves_left_to_turn_on:
        if new_pressure_release_history:
            return new_pressure_release_history
        else:
            return pressure_release_history
    else:
        return pressure_release_history


def day_16_prb_1():
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.DEBUG)
    start_time = time.time()
    logging.info(' day 16, problem 1 '.center(padding_size_large,padding_char))

    # READ INPUT ------------------------------------------------------------------------------
    with open(input_file,'r') as f:
        data = f.read().splitlines()
        
        logging.debug('Reading Input'.center(padding_size_medium,padding_char))
        valves = read_input(data)
        location = 'AA'

    # FIND SHORTEST PATH FROMS FROM ALL VALVES ------------------------------------------------
    logging.getLogger().setLevel(logging.INFO)
    logging.debug('Checking for Unseen Location(s)'.center(padding_size_medium,padding_char))
    
    # key = parent valve name
    # value = dictionary:
    #       key = valve name
    #       value = how many steps way this valve is from the parent valve

    valve_distances = find_valve_distances(valves)

    logging.debug(json.dumps(valve_distances,indent=2))

    # WORK WORK WORK WORK ------------------------------------------------------------
    logging.getLogger().setLevel(logging.DEBUG)
    
    time_limit = 30
    starting_valve = 'AA'
    valves_to_turn_on = [ [name, v.flow_rate ] for name,v in valves.items() if v.flow_rate > 0 ]
    logging.debug(f'{valves_to_turn_on=}')

    # USE THE GIFT EXCHANGE CODE FOR THIS
    # OR USE RECURSION - dept limit: 1000 <<<<<<<<<<< easier for my dead brain

    most_pressure_release_history = valve_permutations(time_limit, starting_valve, valves_to_turn_on, valve_distances)
    most_pressure_released = sum([ v[1] for v in most_pressure_release_history ])
    

    # FINISH ----------------------------------------------------------------------
    logging.info(f'FINISHED------- ')
    logging.info(f'\t{most_pressure_released=}')

    logging.debug(f'--runtime= {datetime.timedelta(seconds=time.time() - start_time)}')
    logging.getLogger().setLevel(previous_logging_level)

def valve_permutations_2(time_left, current_loc_name, valves_left_to_turn_on, valve_distances, explorers=1, _pressure_release_history=[], _itteration=0 ):
    _itteration += 1
    if _itteration >= 10: 
        return _itteration, None
    # pressure_release_history -- List
    #   each item is another list: [ valve_name, pressure_released]

    # valves_left_to_turn_on -- List
    #   each item is another list: [ valve_name, flow_rate]

    if type(time_left) != list: 
        time_left=[time_left] * explorers
    if type(current_loc_name) != list:
        current_loc_name = [current_loc_name] * explorers
    # if _pressure_release_history is None: _pressure_release_history = [ [] for _ in range(explorers) ]
    total_valves = len(_pressure_release_history)+len(valves_left_to_turn_on)
    depth = total_valves-len(valves_left_to_turn_on) # _itteration//explorers
    # explorer_index = _itteration%explorers
    explorer_index = time_left.index(max(time_left))
    logging.debug('|\t'*(depth) + f'i{_itteration}:d{depth}--{time_left=}, explorer={explorer_index}, locs:{current_loc_name}-- {len(valves_left_to_turn_on)=}')
    
    most_pressure_released = 0
    new_pressure_release_history = None
    # temp_pressure_release_history = _pressure_release_history.copy() # don't need this
    
    explorer_current_loc = current_loc_name[explorer_index]
    explorer_time_left = time_left[explorer_index]
    for i,check_valve in enumerate(valves_left_to_turn_on):
        # If we're in the last "group" of valves for the explorers we want to continue to make sure
        # that ALL permutations are chosen, including ones where this explorer doesn't choose a valve 
        #   aka let the others try first
        if i >= len(valves_left_to_turn_on)-explorers and i >= _itteration-explorers:
            _itteration, temp_pressure_release_history = valve_permutations_2(
                time_left,  
                current_loc_name, 
                valves_left_to_turn_on, # Unaltered
                valve_distances, 
                explorers,
                _pressure_release_history,
                _itteration
                )
            if temp_pressure_release_history:
                temp_pressure_released = sum([tmpro[1] for tmpro in temp_pressure_release_history])
                logging.debug('|\t'*(depth) + f'**END FOUND: total={temp_pressure_released}:{temp_pressure_release_history}')
                if temp_pressure_released > most_pressure_released:
                    most_pressure_released = temp_pressure_released
                    new_pressure_release_history = temp_pressure_release_history.copy()
            
        # ---------------------------------------------

        # Temporarily update variables of the explorer to pass to other permutations
        check_valve_name = check_valve[0]
        new_current_loc_name = current_loc_name.copy()
        new_current_loc_name[explorer_index] = check_valve_name
        check_valve_flow_rate = check_valve[1]
        if len(valves_left_to_turn_on) == 0: continue

        time_to_walk_and_turn_on = valve_distances[explorer_current_loc][check_valve_name]+1
        new_time_left = time_left.copy()
        new_time_left[explorer_index] = explorer_time_left-time_to_walk_and_turn_on # -1 to turn on the valve

        if new_time_left[explorer_index] <= 0: continue

        pressure_released = new_time_left[explorer_index] * check_valve_flow_rate
        logging.debug('|\t'*(depth) + f'Moving explorer {explorer_index+1} to: {check_valve} --- {explorer_time_left}-{time_to_walk_and_turn_on}={new_time_left[explorer_index]}, p:{pressure_released}')
        temp_valves_left_to_turn_on = valves_left_to_turn_on.copy()
        del temp_valves_left_to_turn_on[i]

        _itteration, temp_pressure_release_history = valve_permutations_2(
            new_time_left, 
            new_current_loc_name, 
            temp_valves_left_to_turn_on, 
            valve_distances, 
            explorers,
            _pressure_release_history + [[check_valve_name, pressure_released]],
            _itteration
            )
        if temp_pressure_release_history:
            temp_pressure_released = sum([tmpro[1] for tmpro in temp_pressure_release_history])
            logging.debug('|\t'*(depth) + f'**END FOUND: total={temp_pressure_released}:{temp_pressure_release_history}')
            if temp_pressure_released > most_pressure_released:
                most_pressure_released = temp_pressure_released
                new_pressure_release_history = temp_pressure_release_history.copy()

    if valves_left_to_turn_on:
        if new_pressure_release_history:
            return _itteration, new_pressure_release_history
        else:
            return _itteration, _pressure_release_history
    else:
        return _itteration, _pressure_release_history

def day_16_prb_2():
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.DEBUG)
    start_time = time.time()
    logging.info(' day 16, problem 2 '.center(padding_size_large,padding_char))

    # READ INPUT ------------------------------------------------------------------------------
    with open(input_file,'r') as f:
        data = f.read().splitlines()
        
        logging.debug('Reading Input'.center(padding_size_medium,padding_char))
        valves = read_input(data)
        location = 'AA'

    # FIND SHORTEST PATH FROMS FROM ALL VALVES ------------------------------------------------
    logging.debug('Checking for Unseen Location(s)'.center(padding_size_medium,padding_char))
    
    # key = parent valve name
    # value = dictionary:
    #       key = valve name
    #       value = how many steps way this valve is from the parent valve
    valve_distances = find_valve_distances(valves)
    #logging.debug(json.dumps(valve_distances,indent=2))

    # WORK WORK WORK WORK ------------------------------------------------------------
    time_limit = 26
    starting_valves = 'AA'
    valves_to_turn_on = [ [name, v.flow_rate ] for name,v in valves.items() if v.flow_rate > 0 ]
    logging.debug(f'{valves_to_turn_on=}')

    # USE THE GIFT EXCHANGE CODE FOR THIS
    # OR USE RECURSION - dept limit: 1000 <<<<<<<<<<< easier for my dead brain
    logging.debug('-'*30)
    itteractions, most_pressure_release_history = valve_permutations_2(time_limit, starting_valves, valves_to_turn_on, valve_distances, 2)
    most_pressure_released = sum([ v[1] for v in most_pressure_release_history ])
    

    # FINISH ----------------------------------------------------------------------
    logging.info(f'FINISHED------- ')
    logging.info(f'\t{most_pressure_released=}')

    logging.debug(f'--runtime= {datetime.timedelta(seconds=time.time() - start_time)}')
    logging.getLogger().setLevel(previous_logging_level)

if __name__ == '__main__':
    # day_16_prb_1() # Answer is 1460 max pressure released in 30 min 
    day_16_prb_2() 
    # Runtime is like 5minutes
    # WRONG ANSWERS: 
    #   2031 - too low

    # Trying to get the example data answer of 1707