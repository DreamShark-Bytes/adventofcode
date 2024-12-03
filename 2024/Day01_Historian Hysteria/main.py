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
	left_list = []
	right_list = []
	
	total = 0;
	for line in lines:
		lines_read += 1
		
		left, right = [int(s) for s in line.split()]
		left_list.append(left)
		right_list.append(right)
		
		if lines_read <= lines_to_debug:
			logging.debug(f'Line {lines_read}: "{line}", converted to {left} and {right}')

	# Sort the two lists -----------------------------------
	left_list.sort()
	logging.debug("-" * 10 + f"\nLEFT LIST:\n{left_list[:lines_to_debug]}")
	right_list.sort()
	logging.debug("-" * 10 + f"\nLEFT LIST:\n{right_list[:lines_to_debug]}")
	
	# Get the differences ---------------------------------
	if lines_to_debug >= 1: logging.debug("-" * 10 + "\nDIFFERENCES:\n")
	diff_sum = 0
	for n in range(len(left_list)):
		temp = abs(left_list[n] - right_list[n])
		if n <= lines_to_debug:
			logging.debug(f"abs({left_list[n]} - {right_list[n]}) = {temp}")
		diff_sum += temp

	# print answer ----------------------------------------
	logging.info(f'Answer: {diff_sum}');

def part_two(lines, lines_to_debug=0):
	lines_read = 0;
	left_list = []
	right_list = []
	
	total = 0;
	for line in lines:
		lines_read += 1
		
		left, right = [int(s) for s in line.split()]
		left_list.append(left)
		right_list.append(right)
		
		if lines_read <= lines_to_debug:
			logging.debug(f'Line {lines_read}: "{line}", converted to {left} and {right}')
	
	left_list.sort()
	right_list.sort()

	if lines_to_debug >= 1: logging.debug("-" * 10 + "\nSimilarity Score:\n")
	calculations = 0
	similarity_score = 0
	r_index = 0
	for l in left_list:
		left_count = 0
		if calculations <= lines_to_debug:
			logging.debug(f'calc {calculations}: NEW {l} :: ')
		while r_index <= len(right_list)-1 and right_list[r_index] <= l:
			if right_list[r_index] == l: left_count += 1
			r_index += 1
			calculations += 1
			if calculations <= lines_to_debug:
				logging.debug(f'calc {calculations}: ------ r: {right_list[r_index]}')
		calculations += 1
		if calculations <= lines_to_debug:
			logging.debug(f'calc {calculations}: FINISHED {l} :: count {left_count}')
		similarity_score += l * left_count

	# print answer ----------------------------------------
	logging.info(f'Answer: {similarity_score}');

	
def handler():
	logging.getLogger().setLevel(logging.DEBUG)
	
	with open(input_file,'r') as f:
		lines = f.read().split('\n')
	logging.info(' day 1, problem 1 '.center(padding_size_large,padding_char))
	part_one(lines, lines_to_debug=0)

	logging.info(' day 1, problem 2 '.center(padding_size_large,padding_char))
	part_two(lines, lines_to_debug=100)
	
handler()