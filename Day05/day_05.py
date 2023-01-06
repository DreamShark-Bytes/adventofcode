import os
import logging
import re
from collections import defaultdict
logging.basicConfig(level=logging.INFO)
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day_05_input.txt'

def get_stacks(cargo_line):
	start = 1
	increment = 4
	output = []
	for stack_index in range(start, len(cargo_line), increment):
		output.append(cargo_line[stack_index])
	return output
	
def day_05_prb_1():
	logging.info('day 5, problem 1')

	with open(input_file,'r') as f:
		data = f.read().splitlines()
		# data = reader.readlines()
	
		empty_line_index = data.index('')
		logging.info(f'{empty_line_index=}')
		
		labels = get_stacks(data[empty_line_index - 1])
		# Dicitonary
		#	key: label of the stack (just a num 1 - N)
		#	value: 
		#		list of items
		#		first item is on bottom, meaning items moved are at the end. 
		cargo = {}
		for label in labels:
			cargo[label] = []
			
		for stack_str in data[empty_line_index-2::-1]:
			items = get_stacks(stack_str)
			for index, item in enumerate(items):
				if item != ' ':
					cargo[labels[index]].append(item)
			
		logging.info(f'{cargo=}')
		
		moves = data[empty_line_index:]
		for count, move_raw in enumerate(data[empty_line_index + 1:]):
			parts = move_raw.split()
			logging.debug(f'Movement {count + 1} (line {count+2+empty_line_index}),  {parts=}')
			
			mv = int(parts[parts.index('move') + 1])
			frm = parts[parts.index('from') + 1]
			to = parts[parts.index('to') + 1]
			
			# moving items one by one, so we just reverse the list
			items_grabbed = cargo[frm][:-mv-1:-1]
			logging.debug(f'\t moving: {mv}')
			cargo[frm] = cargo[frm][:-mv]
			cargo[to] += items_grabbed
			logging.debug(f'{cargo=}')
			
	final = ''.join([x[-1] for x in cargo.values()])
	print(f'\t{final=}')

def day_05_prb_2():
	logging.info(f'day 5, problem 2')
	
	with open(input_file,'r') as f:
		data = f.read().splitlines()
		# data = reader.readlines()
	
		empty_line_index = data.index('')
		logging.info(f'{empty_line_index=}')
		
		labels = get_stacks(data[empty_line_index - 1])
		# Dicitonary
		#	key: label of the stack (just a num 1 - N)
		#	value: 
		#		list of items
		#		first item is on bottom, meaning items moved are at the end. 
		cargo = {}
		for label in labels:
			cargo[label] = []
			
		for stack_str in data[empty_line_index-2::-1]:
			items = get_stacks(stack_str)
			for index, item in enumerate(items):
				if item != ' ':
					cargo[labels[index]].append(item)
			
		logging.info(f'{cargo=}')
		
		moves = data[empty_line_index:]
		for count, move_raw in enumerate(data[empty_line_index + 1:]):
			parts = move_raw.split()
			logging.debug(f'Movement {count + 1} (line {count+2+empty_line_index}),  {parts=}')
			
			mv = int(parts[parts.index('move') + 1])
			frm = parts[parts.index('from') + 1]
			to = parts[parts.index('to') + 1]
			
			items_grabbed = cargo[frm][-mv:]
			logging.debug(f'\t moving: {mv}')
			cargo[frm] = cargo[frm][:-mv]
			cargo[to] += items_grabbed
			logging.debug(f'{cargo=}')
			
	final = ''.join([x[-1] for x in cargo.values()])
	print(f'\t{final=}')


if __name__ == '__main__':
	day_05_prb_1() # Answer = TWSGQHNHL
	day_05_prb_2() # Answer = JNRSCDWPP