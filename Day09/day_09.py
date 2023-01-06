import os
import json
import copy
import logging

logging.basicConfig(level=logging.INFO)
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day_09_input.txt'

class knot ():
	# location = v, h 
	#		aka v = right/left 
	#			h = up/down)
	
	# example grid: 
	#		 3-- x x x x x
	#		 2-- x x x x x
	#		 0-- x x S x x
	#		-1-- O x x x x
	#		-2-- x x x x x
	#		     | | | | |
	#		    -2-1 0 1 2
	
	# 	directions: 
	# 		up 		^  [+1, 0]
	#		down	v  [-1, 0]
	#		right	>  [0, +1]
	#		left	<  [0, -1]
	
	#	Positions
	#		S = starting position of 0,0
	#		O : v = -1 h = -12

	#					   [v,h]
	def __init__(self, loc=None, history=None):
		if loc is None:
			loc = [0,0]
		self.loc = loc
		
		if history is None:
			history = [] 
			history.append(loc.copy())
		self.history = history	
	
def day_09_prb_1():
	print('day 9, problem 1')
	head = knot()
	tail = knot()
	
	# How much of the world has the knots seen so far
	grid_size = []
	
	with open(input_file,'r') as f:
		data = f.read().splitlines()
		
		for line, command in enumerate(data):
			# if line > 10: continue
			direction, speed = command.split()
			speed = int(speed)
			
			if direction == 'L':
				movement = [0,-1]
			elif direction == 'U':
				movement = [1,0]
			elif direction == 'R':
				movement = [0,1]
			elif direction == 'D':
				movement = [-1,0]
			
			logging.debug(f'{command=}, h{head.loc},m{movement}')
			
			for _ in range(speed):
				old_loc = head.loc.copy()
				head.loc[0] += movement[0]
				head.loc[1] += movement[1]
				logging.debug(f'\t{head.loc=}, {tail.loc=}')
				
				head.history.append(head.loc)
				
				distance = [
					abs(head.loc[0] - tail.loc[0]),
					abs(head.loc[1] - tail.loc[1])
				]
				if 2 in distance:
					tail.loc = old_loc
					tail.history.append(tail.loc)
					logging.debug(f'\tTail moved to: {tail.loc=}')
	
	print(f'{head.loc=}, {tail.loc=}')
	unique_tail_history = [ list(x) for x in set(tuple(x) for x in tail.history) ]
	logging.debug(f'{unique_tail_history=}')
	print(f'{len(unique_tail_history)=}')
	
def visualize_grid(knots, actions):
	previous_logging_level = logging.root.level
	logging.getLogger().setLevel(logging.DEBUG)
	
	logging.debug('-'*20)
	for i, knot in enumerate(knots):
		logging.debug(f'{i=}, {len(knot.history)=}, {knot.history}')
		logging.debug('-'*10)
	
	
	# check last 12 histories
	histories_by_action = '\n'.join([ 
		', '.join([
			str(knot.history[action])
			for knot in knots
		])
		for action in range(len(knots[0].history))
	])
	
	logging.debug(f'Histories by Action: \n{histories_by_action}')
	
	max_v = max([ h[0] for h in knots[0].history])
	min_v = min([ h[0] for h in knots[0].history])
	
	max_h = max([ h[1] for h in knots[0].history ])
	min_h = min([ h[1] for h in knots[0].history ])
	
	logging.debug(f'vert dimensions={min_v}:{max_v}')
	logging.debug(f'horiz dimensions={min_h}:{max_h}')
	
	vertical = max_v - min_v
	horizontal = max_h - min_h
	
	grid_base = [
		[
			'.'
			for h in range(horizontal+1)
		]
		for v in range(vertical+1)
	]
	
	# grid_history = []
	last_action = 0
	overlaps = []

	logging.debug(f'{actions=}')
	logging.debug(f'{knots[0].history=}')

	
	for time_increment in range(len(knots[0].history)):
		if last_action < len(actions) and time_increment >= actions[last_action][1]:
			logging.debug(f'ACTION {last_action}::{actions[last_action][0]} ' + '-'*20)
			last_action += 1

	
		grid = copy.deepcopy(grid_base)
		grid[max_v][abs(min_h)] = 'S'
		
		for knot in range(len(knots)-1, -1, -1):
			h = knots[knot].history[time_increment]
			# print(h)
			char = str(knot) if knot > 0 else "H"

			grid[-1*h[0]+max_v][h[1]-min_h] = char
		
		grid = '\n'.join([ 
			''.join(g)
			for g in grid
		])
		print(grid + "\n")
		# grid_history.append(grid)

	logging.getLogger().setLevel(previous_logging_level)
	# return grid

def day_09_prb_2():
	print('day 9, problem 2')
	
	knots = [ knot() for _ in range(10) ]
	# index: direction, and total-mini-actions 
	actions = []
	total_mini_actions = 1 # knot history starts with default location: [0,0]
	
	with open(input_file,'r') as f:
		data = f.read().splitlines()
		
		for line, command in enumerate(data):
			#if line >20: continue
			direction, speed = command.split()
			speed = int(speed)
			
			actions.append([command, total_mini_actions])
			total_mini_actions += speed

			
			if direction == 'L':
				movement = [0,-1]
			elif direction == 'U':
				movement = [1,0]
			elif direction == 'R':
				movement = [0,1]
			elif direction == 'D':
				movement = [-1,0]
			
			logging.debug('-'*40)
			logging.debug(f'COMMAND {command}, h{knots[0].loc},m{movement}\n')

			for _ in range(speed):
				logging.debug(f'previous location of knot[0]={knots[0].loc}')
				knots[0].loc[0] += movement[0]
				knots[0].loc[1] += movement[1]
				# add loc to history after it moves since the first history is recorded
				knots[0].history.append(knots[0].loc.copy())
				
				logging.debug(f'{knots[0].loc=}')
			
				for k in range(1,len(knots)):
					distance = [
						knots[k-1].loc[0] - knots[k].loc[0],
						knots[k-1].loc[1] - knots[k].loc[1]
					]
					logging.debug(f'\t{k=}, {knots[k].loc} : d{distance}')
					
					'''
					if abs(distance[0])>1 or abs(distance[1])>1: 
						new_loc = knots[k].loc.copy()
						
						# Make distance 1 away from leading knot
						#   keeping in mind the direction of the current knot
						if abs(distance[0])>1: # Vertical
							new_loc[0] = knots[k-1].loc[0] + int(distance[0]/abs(distance[0]) * -1)
						if abs(distance[1])>1: # Horizontal
							new_loc[1] = knots[k-1].loc[1] + int(distance[1]/abs(distance[1]) * -1) 
						knots[k].loc = new_loc.copy()
						
						# if k == len(knots)-1: knots[k].history.append(knots[k].loc)
						
						logging.debug(f'\t\t{k} knot moved to: {knots[k].loc=}')
						break_time = False
					else:
						break_time = True
					'''
					if abs(distance[0])>1 or abs(distance[1])>1:
						if knots[k-1].loc[0] != knots[k].loc[0]:
							knots[k].loc[0] += int(distance[0]/abs(distance[0]))
						if knots[k-1].loc[1] != knots[k].loc[1]:
							knots[k].loc[1] += int(distance[1]/abs(distance[1]))
						logging.debug(f'\t\t{k} knot moved to: {knots[k].loc=}')
					else:
						logging.debug(f'\t\t{k} knot did NOT move, not going further')
						
					# Regardless if the knot moves, 
					# let's put it in history so we know!
					# waiting until the end print grid 
					# so we know the max size. 
					knots[k].history.append(knots[k].loc.copy())
					
					'''
					if break_time:
						logging.debug(f'\t\t{k} knot did NOT move, not going further')
						# break
					'''
	
	# visualize_grid(knots, actions)

	print(f'{knots[0].loc=}, {knots[-1].loc=}')
	unique_tail_history = [ list(x) for x in set(tuple(x) for x in knots[-1].history) ]
	# logging.debug(f'{unique_tail_history=}')
	print(f'{len(unique_tail_history)=}')

if __name__ == '__main__':
	day_09_prb_1() # Answer = 6266
	day_09_prb_2() # Answer = 2369