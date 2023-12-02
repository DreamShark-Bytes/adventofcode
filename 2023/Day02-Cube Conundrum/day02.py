import os
import logging
import time
import re

file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day02_input.txt'
padding_size_large = 100
padding_size_medium = 45
padding_char = '-'

class cube:
	def __init__(self,color,limit,count=0):
		self.color = color
		self.limit = limit
		self.count = count

def color_cube_game(problem_num,lines_to_debug = 0):
	limits = {
		'red':12,
		'green':13,
		'blue':14,
	}
	passing_game_id_count = 0
	total_power = 0
	
	with open(input_file,'r') as f:
		lines = f.read().split('\n')

	lines_read = 0
	for game_played in lines:
		lines_read += 1
		
		pull_results = []

		max_colors = {key:0 for key in limits.keys()}
		
		game_id = int(game_played.split(':')[0][5:])
		pulls = game_played.split(':')[1].split(';')
		id_pass = True
		
		for pull in pulls:
			pull_results += [True]
			pull = [p.strip() for p in pull.split(',')]
			for view in pull:
				view = view.split()
				amount = int(view[0])
				color = view[1]
				
				if amount > max_colors[color]:
					max_colors[color] = amount
				if amount > limits[color]:
					id_pass=False
					pull_results[-1] = False
		game_power = 1
		for value in max_colors.values(): game_power *= value
		total_power += game_power
		
		if id_pass:
			passing_game_id_count +=  game_id
		
		if lines_read <= lines_to_debug:
			logging.debug(f'{game_played}')
			logging.debug('\t' + str(pull_results))
			if id_pass:
				logging.debug('\t' + 'PASS::')
				logging.debug('\t\t' + f'{passing_game_id_count=}')
				logging.debug('\t\t' + f'{max_colors=}')
				logging.debug('\t\t' + f'{game_power=} :: {total_power=}')
	
	if prb_num == 1:
		logging.info(f'ANSWER: {passing_game_id_count=}')
	elif prb_num == 2:
		logging.info(f'ANSWER: {total_power=}')

def handler():
	logging.getLogger().setLevel(logging.DEBUG)
	logging.info(' day 2, problem 1 '.center(padding_size_large,padding_char))
	color_cube_game(problem_num=1) # Answer: 2331
	
	logging.info(' day 2, problem 2 '.center(padding_size_large,padding_char))
	color_cube_game(problem_num=2) # Answer: 71585

handler()