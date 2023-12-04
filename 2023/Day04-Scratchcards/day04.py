import os
import logging
import time
import re

file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day04_input.txt'
padding_size_large = 100
padding_size_medium = 45
padding_char = '-'

def scratch_card(lines_to_debug=0):
	with open(input_file,'r') as f:
		cards = f.read().split('\n')

	prb1_points = 0
	scored_cards = []
	c = 0
	for card in cards:
		
		card_points = 0
		card_id, contents = card.split(':')
		# if I need the numbers:: winning_numbers, card_numbers = [[int(y) for y in x.split()] for x in contents.split('|')]
		winning_numbers, card_numbers = [x.split() for x in contents.split('|')]

		found_numbers = []
		for card_num in card_numbers:
			if card_num in winning_numbers:
				card_points = card_points * 2 if card_points > 0 else 1
				found_numbers.append(card_num)
		if c <= lines_to_debug:
			logging.debug(f'{card_id}::')
		prb1_points += card_points
		card_copies = len(found_numbers)
		scored_cards.append( card_copies )

		c += 1
		if c <= lines_to_debug:
			logging.debug('\t' + f'{card_points=}, {prb1_points=}, {found_numbers=}')
			logging.debug('\t' + f'copies of current card = {card_copies}')
			logging.debug('\t' + f'winning nums found = {len(found_numbers)}')
			
	print(f'{scored_cards[:5]=}')

	'''
	Problem 2 Tactic:
	To avoid re-counting way too many times, we're going to 
	pre-calculate the cards at the end and work our way up
	'''
	prb2_count = 0
	previously_counted = []
	for current in range(len(scored_cards)-1,-1,-1):
		copies_to_be_made = scored_cards[current]
		current_counted = 0
		c = 0
		for pc in previously_counted:
			if c >= copies_to_be_made: break
			current_counted += pc
			c += 1

		current_card_count = 1 + current_counted
		previously_counted.insert(0,current_card_count)
		prb2_count += current_card_count
	
	logging.info(' day 4, problem 1 '.center(padding_size_large,padding_char))
	logging.info(f'Answer: {prb1_points}')

	logging.info(' day 4, problem 2 '.center(padding_size_large,padding_char))
	logging.info(f'Answer: {prb2_count}')
	'''
	Answers
		- 
	'''
 
logging.getLogger().setLevel(logging.DEBUG)
scratch_card(lines_to_debug=196)