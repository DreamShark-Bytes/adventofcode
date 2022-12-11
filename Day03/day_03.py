import os
import logging
import string
logging.basicConfig(level=logging.DEBUG)

def day_03_prb_1():
	logging.info('day 3, problem 1')
	score = 0
	with open('day_03_input.txt','r') as f:
		rucksacks = f.readlines()
		duplicates = []
		priorities = string.ascii_lowercase + string.ascii_uppercase
		priority_score = 0
		print(priorities)

		for count, rucksack in enumerate(rucksacks):
			mid = int(len(rucksack)/2)
			compartment_1 = rucksack[:mid]
			compartment_2 = rucksack[mid:]
			current_dups = []
			
			# Since there is only one item duplicated, 
			# I don't need to check the other compartment
			for item in compartment_1:
				if item in compartment_2 and item not in current_dups:
					current_dups.append(item)

			# There is always a duplicate, no need to check
			duplicates.append(current_dups)
			
			score = priorities.index(current_dups[0]) + 1
			priority_score += score
			
			logging.info(f'Line {count}--- {current_dups[0]=}, {score=}')
			
	print(f'{priority_score=}')

def day_03_prb_2():
	logging.info('day 3, problem 2')
	score = 0
	with open('day_03_input.txt','r') as f:
		rucksacks = f.read().splitlines()
		# rucksacks = f.readlines()
		duplicates = []
		priorities = string.ascii_lowercase + string.ascii_uppercase
		priority_score = 0
		print(priorities)

		for i in range(0,len(rucksacks),3):
			elf_1 = rucksacks[i]
			elf_2 = rucksacks[i+1]
			elf_3 = rucksacks[i+2]
			dups_pass1 = ''
			dups_pass2 = ''
			badge = ''
			
			logging.info(f'Group: {i/3}')
			
			for item in elf_1:
				if item in elf_2 and item not in dups_pass1:
					dups_pass1 += item
			logging.info(f'\t{dups_pass1=}')
			for item in dups_pass1:
				if item in elf_3 and badge == '':
					badge = item
			logging.info(f'\t{dups_pass2=}')	
			logging.info(f'\t{badge=}')
					
			score = priorities.index(badge) + 1
			logging.info(f'\t{score=}')
			priority_score += score
			
			# logging.info(f'Group {i/3}--- {dups_pass1=}, {badge=}')
			
	print(f'{priority_score=}')


if __name__ == '__main__':
	# day_03_prb_1()
	day_03_prb_2()