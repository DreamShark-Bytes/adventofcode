import os
import logging
import time
import re

file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'input.txt'
padding_size_large = 100
padding_size_medium = 45
padding_char = '-'

def part_one(lines,lines_to_debug=0):
	# Read Lines of the file ---------------------------------
	lines_read = 0;

	
	total = 0;
	for line in lines:
		lines_read += 1
		safe_count = 0
		
		levels = [int(s) for s in line.split()]
		previous_level = 0
		slope = 0 # Negative for decline, positive for incline
		safe = True
		for level in levels:
			if slope == 0:
				previous_level = level
				continue
			new_slope = level - previous_level
			if (
				(new_slope<0 and slope>0)
				or (new_slope>0 and slope<0)
				or abs(level - previous_level) <= 3
				):
				safe = False
				break
		if safe: safe_count+=1		
		
		if lines_read <= lines_to_debug:
			logging.debug(f'Line {lines_read}: "{line}", {safe=}')



	# print answer ----------------------------------------
	logging.info(f'Answer: {safe_count}');


	
def handler():
	logging.getLogger().setLevel(logging.DEBUG)
	
	with open(input_file,'r') as f:
		lines = f.read().split('\n')
	logging.info(' day 2, problem 1 '.center(padding_size_large,padding_char))
	part_one(lines, lines_to_debug=10)

	#logging.info(' day 2, problem 2 '.center(padding_size_large,padding_char))

	
handler()