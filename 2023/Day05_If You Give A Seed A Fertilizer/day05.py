import os
import logging
import time
import datetime
import re

file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'sample_input.txt'
input_file = file_path + 'day05_input.txt'
padding_size_large = 100
padding_size_medium = 45
padding_char = '-'

logging.getLogger().setLevel(logging.DEBUG)

def pretty_list_of_lists(l):
	return [[f'{y:,}' for y in x] for x in l]

def read_almanac_prb2(problem_num=2, maps_to_debug=0, seeds_to_debug=0):
	with open(input_file,'r') as f:
		conversions = f.read().split('\n\n')

	if problem_num == 1:
		# Each number in the seeds is treated as a range of 1
		starting_seeds = [[int(x),int(x)+1] for x in conversions.pop(0).split(':')[1].split() ]
	elif problem_num == 2:
		# Seed numbers are grabbed in pairs. First is the start of the Seed ID/Type, 2nd is the number of Seeds for the range
		starting_seeds = conversions.pop(0).split(':')[1].split()
		starting_seeds = [ [int(starting_seeds[x]),int(starting_seeds[x])+int(starting_seeds[x+1])] for x in range(0,len(starting_seeds),2) ]
	else: 
		quit()
	starting_seeds.sort(key=lambda x: x[0])
	
	if maps_to_debug>0: logging.debug(f'Starting Seed ranges = {pretty_list_of_lists(starting_seeds)}')

	# After the Seeds are grabbed we treat each subsequent grouping of numbers as Conversion/Mapping
	# It is assumed they are in sequential order so we ignore the wording, but grab it for debugging purposes.
	almanac = []
	for conversion in conversions:
		conversion = conversion.split('\n')
		header = conversion.pop(0)[:-5]
		processed = []
		for line in conversion:
			processed.append([ int(x) for x in line.split() ])
		processed.sort(key=lambda x: x[1]) # Sort on Source - THIS IS KEY!!!!
		almanac.append([header, processed])

	locations = []
	s = 0

	# Go through map by map w/in the Almanac (not seed by seed, like we did in Problem 1)
	map_being_processed = 0
	sources = starting_seeds
	for map in almanac:
		map_being_processed += 1
		
		header = map[0]
		category_conversion = map[1]
		
		if map_being_processed<=maps_to_debug: logging.debug(f' Map {map_being_processed} : {header}::')
		
		destinations = []
		
		current_source = sources.pop(0)
		c_copy = category_conversion.copy()
		conversion_range = c_copy.pop(0)
		cr_dest_start = conversion_range[0]
		cr_src_start = conversion_range[1]
		cr_length = conversion_range[2]
		cr_src_end = cr_src_start+cr_length

		while current_source and conversion_range:

			conversion_range_consumed = False
			if map_being_processed<=maps_to_debug: 
				logging.debug('\t' + f' -- Comparing: {current_source} to {[cr_src_start,cr_src_end]}')
			# Since we sorted each Category in the Almanac we can do this
			# First take care of unapped source material - the ID's/Type will remain the same.
			if cr_src_start > current_source[0]:
				new_source_end = min(current_source[1],cr_src_start)
				destinations.append([current_source[0],new_source_end])
				
				if current_source[1] <= cr_src_start:
					destinations.append(current_source)
					current_source = sources.pop(0) if sources else []
					if map_being_processed<=maps_to_debug: logging.debug('\t\t' + f' -- NO MAP: source consumed: {destinations[-1]}')
					continue
				else:
					if map_being_processed<=maps_to_debug: logging.debug('\t\t' + f' -- NO MAP: Beginning of source trimmed')
					current_source[0] = cr_src_start

			# Now we grab the middle part where ID's match in this converstion
			if  cr_src_start <= current_source[0] < cr_src_end:
				# Find the difference between the source and destination numbers in this conversion
				diff = cr_dest_start - cr_src_start

				# Find the source range that falls w/in the conversion map we're looking at
				new_source_end = min(current_source[1], cr_src_end)
				src_range_within_conversion = [current_source[0],new_source_end]

				# Apply the conversion and put into the current Destination Range we're building
				destinations.append( [x+diff for x in src_range_within_conversion] )

				# The Current Source is fully consumed by this Mapping
				if current_source[1] <= cr_src_end:
					current_source = sources.pop(0) if sources else []
					if map_being_processed<=maps_to_debug: logging.debug('\t\t' + f' -- source consumed - mapped: {destinations[-1]}')
				# There is still source left my friend. 
				# Adjust current source accordinly and loop again!
				else:
					conversion_range_consumed = True
					
					# Adjust the source since we did find SOME that matched
					current_source[0] = cr_src_end
			else:
				conversion_range_consumed = True
			# Get a new Conversion Mapping Range and loop again!
			if conversion_range_consumed:
				if map_being_processed<=maps_to_debug: logging.debug('\t\t' + f' -- conversion_range consumed')
				conversion_range = c_copy.pop(0) if c_copy else []
				if not conversion_range: continue
				cr_dest_start = conversion_range[0]
				cr_src_start = conversion_range[1]
				cr_length = conversion_range[2]
				cr_src_end = cr_src_start+cr_length

		# Make sure to put any remaining sources into the destinations (incase they weren't mapped)
		sources = destinations+sources if destinations else [current_source]+sources
		sources.sort(key=lambda x: x[0])
		if map_being_processed<=maps_to_debug: logging.debug(f' Mapping complete: {pretty_list_of_lists(sources)}' + '\n')

	logging.info(f'  --Answer: {min([x[0] for x in sources])}')  
	

def read_almanac_prb1(seeds_to_debug=0):
	with open(input_file,'r') as f:
		conversions = f.read().split('\n\n')

	starting_seeds = [int(x) for x in conversions.pop(0).split(':')[1].split() ]
	debug_str = [f'{x:,}' for x in starting_seeds]
	if seeds_to_debug>0: logging.debug(f'Starting Seeds = {debug_str}')

	almanac = []
	for conversion in conversions:
		conversion = conversion.split('\n')
		header = conversion.pop(0)[:-5]
		processed = []
		for line in conversion:
			processed.append([ int(x) for x in line.split() ])
		processed.sort(key=lambda x: x[1]) # Sort on Source
		almanac.append([header, processed])

	locations = []
	s = 0
	for seed in starting_seeds:
		s+=1
		source = seed
		if s<=seeds_to_debug:logging.debug(f'Starting seed: {source:,}')
		c = 0
		for map in almanac:
			header = map[0]
			category_conversion = map[1]
			destination = -1
			c += 1
			if s <= seeds_to_debug: logging.debug('\t' + f'Map {c} : {header}:: {source=:,}')
			for conversion_range in category_conversion:
				cr_destination_start = conversion_range[0]
				cr_source_start = conversion_range[1]
				range_len = conversion_range[2]
				if s <= seeds_to_debug: logging.debug('\t\t' + f'{cr_source_start:,}--{cr_source_start + range_len:,} :: {cr_destination_start:,}')

				# since we sorted we can do this
				if cr_source_start > source:
					break
				if cr_source_start <= source < cr_source_start+range_len:
					destination = source-cr_source_start + cr_destination_start
					break
			if destination == -1: 
				destination = source
				if s <= seeds_to_debug: logging.debug('\t\t\t' + f'--- NO CHANGE: {source:,}')
			else:
				if s <= seeds_to_debug: logging.debug('\t\t\t' + f'--- !!!!!: {source:,} >> {destination:,}')
			
			source = destination
		if s <= seeds_to_debug: logging.debug('\t' + f'RESULT::::: {source:,}')
		locations.append(source)

	logging.info(f'  --Answer: {min(locations)}')  

def handler():
	start_time = time.time()
	logging.info(' day 5, problem 1 '.center(padding_size_large,padding_char))
	read_almanac_prb1(0) # Answer: 218,513,636
	logging.debug(f' --runtime= {datetime.timedelta(seconds=time.time() - start_time)}')

	start_time = time.time()
	logging.info(' day 5, problem 2 '.center(padding_size_large,padding_char))
	read_almanac_prb2() # Answer: 81956384
	logging.debug(f' --runtime= {datetime.timedelta(seconds=time.time() - start_time)}')

handler()
