import os
import logging
import time
import datetime
import re

# Configurations -------------------------------- 
day = 6
sample_input = False
logging.getLogger().setLevel(logging.DEBUG)

# Global Variables ------------------------------
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = 'sample_input.txt' if sample_input else 'input.txt'  # f'day{day:02d}_input.txt'
input_file = file_path + input_file

races = [[7,9],[15,40],[30,200]] if sample_input else [[49,263],[97,1532],[94,1378],[94,1851]]

padding_size_large = 100
padding_size_medium = 45
padding_char = '-'

def optimize_race(problem_num, races_to_debug=0):
	with open(input_file,'r') as f:
		races = [x.split(':')[1] for x in f.read().split('\n')]
		
		if problem_num == 1:
			races = [[int(y) for y in x.split()] for x in races]
			new_data = []
			for i in range(len(races[0])):
				new_data.append( [races[0][i], races[1][i]] )
			races = new_data
		elif problem_num == 2:
			races = [[ int(''.join([ y  for y in x if y.isdigit()])) for x in races]]

	record_beating_results = []

	r = 0
	for race in races:
		r += 1
		
		time = race[0]
		distance_record = race[1]

		if r<=races_to_debug: logging.debug(f'Race: {r}: Record: {distance_record}')

		new_record_count = 0
		for hold_time in range(1,time-1):
			# Distance = initial_velocity * time + 1/2 accelleration * time
			distance_travelled = 1/2 * hold_time * (time - hold_time)**2 # wrong b/c velocity is a constant??
			distance_travelled = hold_time * (time - hold_time)

			if r<=races_to_debug: logging.debug('\t' + f'Time: {hold_time} -- Distance: {distance_travelled}')
			if distance_travelled > distance_record:
				new_record_count += 1
				if r<=races_to_debug: logging.debug('\t\t' + f'-- NEW RECORD, {new_record_count}')
			else:
				if r<=races_to_debug: logging.debug('\t\t' + f'-- Boo')
		record_beating_results.append(new_record_count)
	logging.debug(f'New_records: {record_beating_results}')

	margin_of_error = 1
	for new_record_count in record_beating_results:
		margin_of_error *= new_record_count

	logging.info(f'  --Answer: {margin_of_error}')  

def optimize_race_prb2(problem_num=2, lines_to_debug=0):
	with open(input_file,'r') as f:
		conversions = f.read().split('\n\n')

	logging.info(f'  --Answer: {-1}')  
	

def handler():
	problems = {
		'1' : lambda: optimize_race(problem_num=1), # Answer is: 4403592
		'2' : lambda: optimize_race(problem_num=2) # Answer: 38017587, took 8 seconds to run
	}
	for prb_num, prb in problems.items():
		start_time = time.time()
		logging.info(f' day {day}, problem {prb_num} '.center(padding_size_large,padding_char))
		prb()
		logging.debug(f' --runtime= {datetime.timedelta(seconds=time.time() - start_time)}')


handler()
