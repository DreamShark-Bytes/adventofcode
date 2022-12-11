import os
import logging
from math import prod
logging.basicConfig(level=logging.INFO)

'''
ASSUMPTIONS
1. grid is uniform 
	aka rows are always the same length compared to eachotgher
	and no empty values
'''

def day_08_prb_1():
	print('day 8, problem 1')
	visible_tree_count = 0
	visible_trees = []
	
	with open('day_08_input.txt','r') as f:
		data = f.read().splitlines()
		# data = f.readlines()[0]
		
		logging.info(f'Grid Size: w{len(data)}, h{len(data[0])}')
		
		# initial count of visible trees from the grid's paremeter
		visible_tree_count = len(data[0]) * 2 + (len(data)-2) * 2
		#visible_tree_count = 0
		
		for orientation in ['Horizontal','Vertical']:
			visible_trees_orientation = [] # grid = x,y
			if  orientation=='Horizontal':
				get_treeline = data
			else: # Vertical
				get_treeline = [
						''.join([
							data[x][y]
							for x in range(len(data))
						])
						for y in range(len(data[i]))
					]
				# print(get_treeline)
			
			orientation_length = len(data) if orientation=='Horizontal' else len(data[0])
			for i in range(orientation_length):
				if i == 0 or i == orientation_length-1: continue
				# if i >= 2: continue
				# if orientation == 'Vertical': continue

				logging.debug('-'*50)
				tree_line = get_treeline[i]
				logging.debug(f'{orientation}-{i=}--{tree_line=}')
				
				# increment = 1 means starting left, going right
				# othwerise -1 means starting right, going left.
				for increment in [1,-1]:
					if increment>0:
						s = "Left" 
						highest_tree_value = tree_line[0]
					else:
						s = "Right"
						highest_tree_value = tree_line[-1]
					
					temp_visible_trees = []

					logging.debug(f'Checking from {s} side')
					for k in range(1, orientation_length-1):
						j = k if increment>0 else len(tree_line)-k-1
						
						if orientation == 'Horizontal':
							x = i
							y = j 
						else: # Vertical
							x = j 
							y = i 
						
						logging.debug(f'checking tree: {x=}:{y=}-- is {data[x][y]} > {highest_tree_value}')
						
						if data[x][y] > highest_tree_value:
							tree = [x,y]
							temp_visible_trees.append(str(tree))
							highest_tree_value = data[x][y]
					logging.debug(f'\tVisible trees: {temp_visible_trees}')
					visible_trees_orientation += temp_visible_trees
			visible_trees += visible_trees_orientation
			logging.info(f'Visible tree count from {orientation}: {len(visible_trees_orientation)}')
	logging.debug('-'*50)
	logging.info(f'visible trees from perimeter: {visible_tree_count}')
	# print(visible_trees)
	logging.info(f'{len(visible_trees)=}')
	visible_trees.sort()
	visible_trees = set(visible_trees)
	logging.info(f'unique trees: {len(visible_trees)}')
	visible_tree_count += len(visible_trees)
	
	print(f'{visible_tree_count=}')

def day_08_prb_2():
	print('day 8, problem 2')
	scenic_scores = []
	cardinal_directions = ['Up', 'Left', 'Down', 'Right'] # match the problem description
	
	
	with open('day_08_input.txt','r') as f:
		data = f.read().splitlines()
		
		scenic_scores = [ [x, y, -1, [] ] for x in range(len(data))  for y in range(len(data[0])) ]
		# limit = len(data[0])
		
		logging.debug(f'Grid Size: w{len(data)}, h{len(data[0])}')
		
		logging.debug(f'{len(scenic_scores)=}')
		logging.debug(f'{len(scenic_scores[0])=}')
		
		logging.debug(f'{cardinal_directions=}')
		
		for i, tree in enumerate(scenic_scores):
			# if i < limit or i >= limit*2: continue
			
			# X = Left & Right
			tree_x = tree[0]
			# Y = Up & Down
			tree_y = tree[1]
			tree_height = int(data[tree_y][tree_x])
			scenic_scores[i][2] = tree_height
			
			logging.debug(f'{i=}:{tree}')
			
			for direction in cardinal_directions:
				logging.debug(f'\t{direction=}')
				delta = 0
				score = 0
				limit_not_found = True
				
				if direction=='Up':
					out_of_bounds = lambda d: tree_y-d < 0
					get_height = lambda d: int(data[tree_y-d][tree_x])
				elif direction=='Down':
					out_of_bounds = lambda d: tree_y+d >= len(data[0])
					get_height = lambda d: int(data[tree_y+d][tree_x])
				elif direction=='Left':
					out_of_bounds = lambda d: tree_x-d < 0
					get_height = lambda d: int(data[tree_y][tree_x-d])
				elif direction=='Right':
					out_of_bounds = lambda d: tree_x+d >= len(data[0])
					get_height = lambda d: int(data[tree_y][tree_x+d])
					
				while limit_not_found:
					delta += 1
					
					if out_of_bounds(delta):
						limit_not_found = False
					else: 
						compare_height = get_height(delta)
						
						logging.debug(f'\t\t{delta=}--{compare_height=}')
							
					if limit_not_found:
						score += 1
						if tree_height <= compare_height:
							limit_not_found = False
				scenic_scores[i][3].append(score)
				
	# print(f'{scenic_scores[99:198]=}')
	scores = [ prod(x[3]) for x in scenic_scores ]
	scores.sort(reverse=True)
	print(scores[:10])
	
	scenic_scores.sort(key=lambda x: prod(x[3]),reverse=True)
	logging.dbug(scenic_scores[:10])

if __name__ == '__main__':
	# day_08_prb_1()
	day_08_prb_2()