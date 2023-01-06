import os
import logging
import json
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('my-logger')
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day_07_input.txt'

class item():
	def __init__ (self, level, path, name, my_type, size , line = None):
		self.level = level
		self.path = path
		self.name = name
		self.my_type = my_type
		self.size = size
		self.line = line

def item_doest_exists(new_item, tree):
	name = new_item.name
	path = new_item.path
	level = new_item.level
	if (
			name not in 
			[ 
				x.name 
				for x in tree 
				if 
					x.path == path 
			]
		):
		return True
	else:
		return False
		
def find_dir_sizes(tree, path=[]):
	previous_logging_level = logging.root.level
	logging.getLogger().setLevel(logging.INFO)
	logging.debug(f'level {len(path)}, {path=}')
	
	# Get index of children
	children = [
		i 
		for i in range(len(tree))
		if (
			tree[i].path == path 
	)]

	# logging.debug(f'children = {[ tree[x].name for x in children ]}')
	children.sort(key=lambda i: tree[i].name)
	logging.debug(f'\tchildren = {[ tree[x].name for x in children ]}')
	
	output = []
	size = 0
	
	for i in children:
		child = tree[i]
		logging.debug(f'child={json.dumps(child.__dict__, indent=2)}')
		if child.my_type == 'dir':
			child_children, size_of_children, tree = find_dir_sizes(tree, path=child.path + [child.name])
			
			# size_of_children = sum([ tree[x].size for x in child_children ])
			if not tree[i].size:
				tree[i].size = size_of_children
			size += size_of_children
			
			s = f'- {child.name} (dir, {size_of_children})'
			output.append(s)
			
			logging.debug(f'path={child.path},level={len(child.path)}--{child_children=}')
			output += [ '|\t' + x for x in child_children ]
			
		else: # type == 'file'
			s = f'- {child.name} (file, {child.size})'
			output.append(s)
			size += child.size
		
	if len(path) == 0:
		output = '\n'.join(output)
		logging.getLogger().setLevel(previous_logging_level)
		
	return output, size, tree
	
	
	
# Assuming that a 'cd' command ONLY opens an existing folders
def day_07():	
	with open(input_file,'r') as f:
		data = f.read().splitlines()
		# data = f.readlines()
		
		# each item is a dictionary: 
		#	level = what level of the directory tree
		#	path = full folder path to get to this item 
		#		(last item is current parent)
		#	name = name of the file or directory
		#	type = file or dir (for directory)
		#	size (directory to be determined later)
		dir_tree = []
		current_path = []
		new_item = {}
		
		for l, output_raw in enumerate(data):
			line = l + 1
			#if line >= 20: break
			
			#if line >= 690 and line <= 720:
			if line <=-1:
				# logger.propagate = True
				logging.getLogger().setLevel(logging.DEBUG)
			else:
				# logger.propagate = False
				logging.getLogger().setLevel(logging.INFO)
			
			output = output_raw.split()
			logging.debug('-'*75)
			logging.debug(f'{line=} :: {output=}')
			
			item_size = None
			item_type = None
			
			# is a command
			if output[0] == '$': 
				# should list directories next
				if output[1] == 'ls':
					continue
				# change directory
				elif output[1] == 'cd': 
					if output[2] == "..":
						old_level = len(current_path)
						temp = current_path.pop()
					else:
						old_level = len(current_path)
						item_name = output[2]
						
						# Must record this before updating path
						new_item = item(
							level = old_level,
							path = current_path.copy(),
							name = item_name,
							my_type = "dir",
							size = item_size
						)
						
						current_path.append(item_name)
						
						not_exists = item_doest_exists(new_item, dir_tree)
					
					logging.debug(f'\tFOLDER PATH (len {len(current_path)}={json.dumps(current_path,indent=2)}')

					
					# only record new directory if we're not going back up the tree
					# aka '..'
					if output[2] == "..": 
						continue
			else:
				# ADD NEW ENTRY HERE TOO
				if output[0] == 'dir':
					item_type = 'dir'
				else:
					item_type = 'file'
					item_size = int(output[0])
				item_name = output[1]
				new_item = item(
					level = len(current_path),
					path = current_path.copy(),
					name = item_name,
					my_type = item_type,
					size = item_size
				)
				not_exists = item_doest_exists(new_item, dir_tree)
				
			logging.basicConfig(level=logging.WARNING)
			
			logging.debug(f'\tItem Doesnt Exist = {not_exists}')
			new_item.line = line
			if not_exists:
				logging.debug(f'\tAdding New Item: {json.dumps(new_item.__dict__, indent=10)}')
				dir_tree.append(new_item)
			elif new_item.my_type == 'file':
				previous_item = [ 
					x.line 
					for x in dir_tree 
					if 
						x.name==new_item.name 
						and x.path == new_item.path
					]
				logging.warning(f'{line=} --file appeared twice: {new_item.__dict__}')
				logging.warning(f'\t{previous_item=}')
	
	logging.getLogger().setLevel(logging.DEBUG)
	pretty_tree, total_size, dir_tree = find_dir_sizes(dir_tree)

	logging.debug('PRETTY TREE: \n' + pretty_tree)
	
	# logging.debug(f'TREE: {json.dumps(dir_tree, indent = 2)}')
	logging.info(f'File count: {len([ x for x in dir_tree if x.my_type=="file" ])}')
	logging.info(f'Directory count: {len([ x for x in dir_tree if x.my_type=="dir" ])}')

	empty_score_dirs = [ x.name for x in dir_tree if (x.size == 0 or not x.size) and x.my_type=='dir' ]
	if empty_score_dirs: logging.warning(f'{empty_score_dirs=}')
	
	empty_score_files = [ x.name for x in dir_tree if (x.size == 0 or not x.size) and x.my_type=='file']
	if empty_score_files: logging.warning(f'{empty_score_files=}')
	
	logging.debug('-'*75)
	day_07_prb_1(dir_tree)
	
	logging.debug('-'*75)
	day_07_prb_2(dir_tree)

def day_07_prb_1(dir_tree):
	print('day 7, problem 1')
	items = [ x for x in dir_tree if x.size <= 100000 and x.my_type == 'dir' ]
	dir_sizes_conditional = [ x.size for x in items ]
	# logging.debug('-'*75)
	logging.info(f'Directories that met SIZE criteria: {len(items)}')
	# logging.debug(f'{json.dumps(items, indent=2)}')
	
	size_sum = sum(dir_sizes_conditional)
	print(f'{size_sum=}')

def day_07_prb_2(dir_tree):
	print('day 7, problem 2')
	
	diskspace = 70000000
	desired_unused_space = 30000000
	max_used_space = diskspace - desired_unused_space
	print(f'{max_used_space=}')
	
	root = [ x for x in dir_tree if x.path == [] ] [0]
	print(f'{root.size=}')
	
	distances = [ x for x in dir_tree if root.size - x.size <= max_used_space and x.my_type == 'dir' ]
	distances.sort(key= lambda x: root.size - x.size, reverse=True)
	
	# distances = [ x.__dict__ for x in distances  ]
	# print(f'Solutions--\n{json.dumps(distances[:5],indent=2)}')
	distances = [ f'{d.name=}, {d.size=}, space if del: {root.size - d.size}' for d in distances  ]
	print(f'Solutions--\n{json.dumps(distances[:20],indent=2)}')
	

if __name__ == '__main__':
	day_07()
	# Problem 1 Answer = 1844187
	# Problem 2 Answer = 4978279