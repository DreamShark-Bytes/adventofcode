import os
import logging
# logging.basicConfig(level=logging.DEBUG)

def day_01_prb_1():
	logging.info('day 1, problem 1')
	max_user = 0
	current_user = 0
	with open('day_01_input.txt','r') as reader:
		data = reader.read().splitlines()
		# data = reader.readlines()
		for line in data:
			if line:
				current_user += int(line)
			else:
				if current_user > max_user:
					max_user = current_user
				current_user = 0
	print(f'{max_user=}')
	
def day_01_prb_2():
	logging.info('day 1, problem 2')
	elf_calories = []
	current_elf = 0
	# Same input as Problem 1
	with open('day_01_input.txt','r') as f:
		data = f.read().splitlines()
		for line in data:
			if line:
				current_elf += int(line)
			else:
				elf_calories.append(current_elf)
				current_elf = 0
	elf_calories.sort(reverse=True)
	logging.info(f'{elf_calories=}')
	top_3 = elf_calories[:3]
	logging.info(f'{top_3=}')
	print(f'{sum(top_3)=}')

if __name__ == '__main__':
	day_01_prb_2()