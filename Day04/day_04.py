import os
import logging
import re
logging.basicConfig(level=logging.INFO)
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day_04_input.txt'

def day_04_prb_1():
	logging.info('day 4, problem 1')

	with open(input_file,'r') as f:
		pairings = f.readlines()
	
		encapsulations = []

		for count, pair in enumerate(pairings):
			p1_start, p1_end, p2_start, p2_end = [ int(x) for x in re.split(',|-',pair) ]
			encap = False
			
			if (
					p1_start <= p2_start and p1_end >= p2_end 
					or p2_start <= p1_start and p2_end >= p1_end
				):
				encapsulations.append(count)
				encap = True
			
			logging.debug(f'Line {count}--- {p1_start}-{p1_end},{p2_start}-{p2_end} :: {encap=}')
			
	print(f'\t{len(encapsulations)=}')

def day_04_prb_2():
	logging.info(f'day 4, problem 2')
	
	with open(input_file,'r') as f:
		pairings = f.readlines()
	
		overlaps = []

		for count, pair in enumerate(pairings):
			p1_start, p1_end, p2_start, p2_end = [ int(x) for x in re.split(',|-',pair) ]
			olap = False
			
			if (
					p1_start <= p2_end and p1_end >= p2_end 
					or p2_start <= p1_end and p2_end >= p1_end
				):
				overlaps.append(count)
				olap = True
			
			logging.debug(f'Line {count}--- {p1_start}-{p1_end},{p2_start}-{p2_end} :: {olap=}')
			
	print(f'\t{len(overlaps)=}')


if __name__ == '__main__':
	day_04_prb_1() # Answer = 571
	day_04_prb_2() # Answer = 917