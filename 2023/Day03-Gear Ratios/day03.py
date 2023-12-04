import os
import logging
import time
import re
import math

file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day03_input.txt'
padding_size_large = 100
padding_size_medium = 45
padding_char = '-'

gear_char = '*'

def distance(pos1,pos2):
	r = 0
	for d in range(len(pos1)):
		r += (pos1[d] - pos2[d])**2
	return math.sqrt(r)

def find_symbols(lines, looking_for=lambda x: x,lines_to_debug = 0):
	found_symbols = [] 
	gear_ratio_map = []
	for x in range(len(lines)):
		gear_ratio_map.append([])
		line = lines[x]
		for y in range(len(line)):
			char = line[y]
			gear_ratio_map[x].append(None)
			if looking_for(char):
				if x <= lines_to_debug:
					logging.debug(f'Line {x}: {char} at column {y}')
				found_symbols.append([x,y])

				gear_ratio_map[x][y] = [1,0]

		if x < lines_to_debug: logging.debug(padding_char * padding_size_medium)
	return found_symbols,gear_ratio_map

def analyse_schematic(lines, lines_to_debug = 0):
	# Loop once to find symbols (need to know what is ahead)
	symbol_map, gear_map = find_symbols(lines, lambda c: not c.isalnum() and c != '.',lines_to_debug)
	if lines_to_debug > 0: logging.debug(padding_char * padding_size_large)

	part_sum = 0
	# Loop again to find numbers
	current_num = ''
	max_dist_num_to_symbl = 1.5  # aka sqrt(2) > x > sqrt(3)
	good_num_dist = False

	max_dist_symbl_ratio = 1.5 
	good_symbl_dist = False
	all_found_symbols = []
	found_symbols = []

	for x in range(len(lines)):
		line = lines[x]
		for y in range(len(line)):
			char = line[y]
			if not char.isdigit() and current_num != '':
				current_num = int(current_num)

				if x < lines_to_debug:
					logging.debug(f'Line {x}: {current_num} :: {good_num_dist}')
					if good_num_dist: logging.debug('\t' + f'-adding to {part_sum}')

				unique_symbols = []
				if good_symbl_dist:
					for fs in found_symbols:
						if not any(us == fs for us in unique_symbols):
							gear_map[fs[0]][fs[1]][1]+=1 # count
							if gear_map[fs[0]][fs[1]][1] <= 2:
								gear_map[fs[0]][fs[1]][0]*=current_num # gear_ratio
							unique_symbols.append(fs)
					all_found_symbols.append(unique_symbols)
					good_symbl_dist = False
					found_symbols = []
				
				part_sum += int(current_num) if good_num_dist else 0
				good_num_dist = False

				current_num = ''
			elif char.isdigit():
				current_num += char 
				for symbol_loc in symbol_map:
					d = distance([x,y], symbol_loc)
					if d <= max_dist_num_to_symbl: 
						good_num_dist = True
					if gear_map[symbol_loc[0]][symbol_loc[1]] != None and d <= max_dist_symbl_ratio:
						good_symbl_dist = True
						found_symbols.append(symbol_loc)

		if x < lines_to_debug: logging.debug(padding_char * padding_size_medium)
	
	ratio_sum = 0
	for x in gear_map:
		for y in x:
			if y and y[1] == 2:
				ratio_sum += y[0]

	logging.info(f'Problem 1 ---Answer: {part_sum}') # Answer: 517021
	logging.info(f'Problem 2 ---Answer: {ratio_sum}') # Answer: 81296995

def handler():
	logging.getLogger().setLevel(logging.DEBUG)
	with open(input_file,'r') as f:
		lines = f.read().split('\n')

	logging.info(' day 2 '.center(padding_size_large,padding_char))
	analyse_schematic(lines) 

handler()