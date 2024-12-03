import os
import logging
import time
import datetime
import math

# Configurations -------------------------------- 
day = 7
sample_input = False
# logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

# Global Variables ------------------------------
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = 'sample_input.txt' if sample_input else 'input.txt'  # f'day{day:02d}_input.txt'
input_file = file_path + input_file

padding_size_large = 100
padding_size_medium = 45
padding_char = '-'

def endless_substring(string, start_index, length):
	# Incase the pattern wraps around the string, let's figure that out
	if start_index+length > len(string):
		pattern = string[x:len(string)] + string[:length-(len(string)-start_index)-1]
	else:
		pattern = string[start_index: start_index+length]
	new_start_index = (start_index+length)%len(string)
	return pattern, new_start_index

# assumes string is repeating enlessly
# while we can find patterns beyond the given string, 
# we're limiting scope to the length of the string
def repeating_patterns(string):
	# Each pattern is a sub-list
	# 	index 0: starting index of pattern in string
	#	index 1: length of the pattern
	#	index 2: the pattern itself for debugging
	patterns = []
	
	print(f'{len(string)=} :: string="{string}"')
	for length in range(1,len(string)+1):
		print('|\t' + f'current length check :: {length}')
		# don't need to check entire string each time, only the length of characters we're looking at
		for variation in range(length):
			# For each pattern we look for the recurring starting indexes to know a pattern is repeating_patterns
			# Used only when a pattern wraps around a string
			checked_indexes = []
			
			pattern_base, new_start_index = endless_substring(string, variation, length)
			print('|\t|\t' + f'- {variation=} :: {new_start_index=} :: pattern = "{pattern_base}"')
			
			recurring = True
			while recurring:
				current_cut, new_start_index = endless_substring(string, new_start_index, length)
				if current_cut != pattern_base:
					# or new_start_index in checked_indexes:
					recurring = False
				recurring = False
			
		if length >= 10: quit()
			

def follow_map(problem_num, debug_steps=0):
	with open(input_file,'r') as f:
		step_directions, temp_nodes = f.read().split('\n\n')
	nodes = {}
	for node in temp_nodes.split('\n'):
		key, paths = node.split(' = ')
		nodes[key] = paths[1:-1].split(', ')
	temp_nodes = ''
	
	if problem_num==1:
		starting_locs = [ x for x in nodes.keys() if x=='AAA'] # list all the starting locations
		goal_condition = lambda x: x=='ZZZ' # each cuyrrent location must match this lambda
	elif problem_num==2:
		starting_locs = [ x for x in nodes.keys() if x[-1]=='A'] # list all the starting locations
		goal_condition = lambda x: x[-1]=='Z' # each cuyrrent location must match this lambda
	meets_goal = lambda x: False not in [goal_condition(y) for y in x ]
	
	
	if debug_steps>0:
		# logging.debug(nodes)
		logging.debug(step_directions)
		logging.debug(f'{starting_locs=}::goals={[x for x in nodes.keys() if goal_condition(x)]}')
		
	current_locs = starting_locs
	goal_found = False
	step_count = 0
	while not goal_found: 
		for step_direction in step_directions: 
			prev_locs = current_locs.copy()
			current_locs = []
			step_count += 1
			if step_count<= debug_steps: logging.debug(f'-- {step_count:,} :: {step_direction}')
			for c_loc in prev_locs:
				if step_direction=='R':
					current_locs.append(nodes[c_loc][1])
				elif step_direction=='L':
					current_locs.append(nodes[c_loc][0])
			if step_count <= debug_steps: 
				for loc_index in range(len(current_locs)):
					logging.debug('\t' + f'--{prev_locs[loc_index]} ---> {current_locs[loc_index]}')
			else:
				print(f'-- {step_count:,} :: {step_direction}', end='\r')
			if meets_goal(current_locs):
				goal_found=True
				break
	print(f'Steps to goal: {step_count:,}')
	
def follow_map_2(problem_num, debug_steps=0):
	with open(input_file,'r') as f:
		step_directions, temp_nodes = f.read().split('\n\n')
	nodes = {}
	for node in temp_nodes.split('\n'):
		key, paths = node.split(' = ')
		nodes[key] = paths[1:-1].split(', ')
	temp_nodes = ''
	
	if problem_num==1:
		starting_locs = [ x for x in nodes.keys() if x=='AAA'] # list all the starting locations
		goal_condition = lambda x: x=='ZZZ' # each cuyrrent location must match this lambda
	elif problem_num==2:
		starting_locs = [ x for x in nodes.keys() if x[-1]=='A'] # list all the starting locations
		goal_condition = lambda x: x[-1]=='Z' # each cuyrrent location must match this lambda
	meets_goal = lambda x: False not in [goal_condition(y) for y in x ]
	
	
	if debug_steps>0:
		# logging.debug(nodes)
		logging.debug(step_directions)
		logging.debug(f'{starting_locs=}::goals={[x for x in nodes.keys() if goal_condition(x)]}')
		
	current_locs = starting_locs
	goal_found = False
	step_count = 0
	while not goal_found: 
		for step_direction in step_directions: 
			prev_locs = current_locs.copy()
			current_locs = []
			step_count += 1
			if step_count<= debug_steps: logging.debug(f'-- {step_count:,} :: {step_direction}')
			for c_loc in prev_locs:
				if step_direction=='R':
					current_locs.append(nodes[c_loc][1])
				elif step_direction=='L':
					current_locs.append(nodes[c_loc][0])
			if step_count <= debug_steps: 
				for loc_index in range(len(current_locs)):
					logging.debug('\t' + f'--{prev_locs[loc_index]} ---> {current_locs[loc_index]}')
			else:
				print(f'-- {step_count:,} :: {step_direction}', end='\r')
			if meets_goal(current_locs):
				goal_found=True
				break
	print(f'Steps to goal: {step_count:,}')

def handler():
	problems = {
		'1' : lambda: follow_map(problem_num=1), # Answer is 12,737
		'2' : lambda: follow_map(problem_num=2, debug_steps=5) 
	}
	for prb_num, prb in problems.items():
		start_time = time.time()
		logging.info(f' day {day}, problem {prb_num} '.center(padding_size_large,padding_char))
		prb()
		logging.debug(f' --runtime= {datetime.timedelta(seconds=time.time() - start_time)}')


handler()
