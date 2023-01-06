import os
import logging
logging.basicConfig(level=logging.INFO)
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day_06_input.txt'

def day_06_prb_1():
	logging.info('day 6, problem 1')
	
	with open(input_file,'r') as f:
		#data = f.read().splitlines()
		data = f.readlines()[0]
		start = 0
	
		for count, char in enumerate(data):
			if count < 3: 
				continue
			
			logging.debug(f'{count=}--{char=}')
			key = data[count-3:count + 1]
			logging.debug(f'\t{key=}')
			uniques = set(key)
			start_of_packet = len(key) == len(uniques)
			logging.debug(f'\t{start_of_packet=}')

			if start_of_packet: 
				start_of_packet = count + 1
				break
			
	print(f'\t{start_of_packet=}')

def day_06_prb_2():
	logging.info('day 6, problem 2')
	
	with open(input_file,'r') as f:
		#data = f.read().splitlines()
		data = f.readlines()[0]
		marker_len = 14
		start = 0

		for count in range(marker_len - 1, len(data)):
			logging.debug(f'CHARACTER={count}')
			key = data[count-marker_len+1:count + 1]
			logging.debug(f'\t{key=}')
			uniques = set(key)
			start_of_marker = len(key) == len(uniques)
			logging.debug(f'\t{start_of_marker=}')

			if start_of_marker: 
				start_of_marker = count + 1
				break
			
	print(f'\t{start_of_marker=}')

if __name__ == '__main__':
	day_06_prb_1() # Answer = 1582
	day_06_prb_2() # Answer = 3588