import os
import logging
import time
import datetime
import re
import pprint

# Configurations -------------------------------- 
day = 7
sample_input = False
# logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

# Global Variables ------------------------------
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = 'sample_input.txt' if sample_input else 'input.txt'  # f'day{day:02d}_input.txt'
input_file = file_path + input_file

padding_size_large = 100
padding_size_medium = 45
padding_char = '-'

class deck_class:
	unique_cards = [] # Must be in order of "scores better"
	deck_base = 1
	def __init__(self, unique_cards):
		self.unique_cards = unique_cards
		self.base = len(unique_cards)

# Since we're going through each card, one by one, we're goign to take this
# opportunity to calculate the subscore - aka which card is the highest
# going left to right.
# To do this we create a number system using the base as the number of unique cards
# our normal number system is base10, this is base13
#
# There is an easier way to do this, but I liked learning how to do it this way
def hand_subscoring(cards, deck, debug_hand=False):
	previous_logging_level = logging.root.level
	logging.getLogger().setLevel(logging.INFO)

	sub_score = 0
	for c in range(len(cards)):
		card = cards[c]
		card_score = deck.unique_cards.index(card)
		position_base = deck.base ** (len(cards)-1 - c)
		sub_score += card_score * position_base
		logging.debug('\t\t' + f'card #{c}:"{card}" -- score = {card_score}*{position_base}={card_score * position_base}')
	
	logging.getLogger().setLevel(previous_logging_level)
	return sub_score

def count_cards (cards,deck):
	card_counts={}
	for card in cards:
		if card in card_counts.keys():
			card_counts[card] += 1
		else:
			card_counts[card] = 1
	card_counts = [[key,value] for key,value in card_counts.items()]
	card_counts.sort(key=lambda x:x[1]*deck.base + deck.unique_cards.index(x[0]),reverse=True)
	return card_counts

def handle_wild_card(cards, card_counts, deck,debug_hand):
	wild_card = 'J'

	if wild_card not in cards: return cards
	if debug_hand: logging.debug('\t\t' + f'Wild card ({wild_card}) found')
	wild_card_i = cards.index(wild_card)
	if card_counts[0][0] == wild_card:
		largest_non_wild = card_counts[0][0]
	else:
		largest_non_wild = card_counts[1][0]

	# TODO: to handle "Two Pair": ACCOUNT for cards AFTER wild_card - just grab "highest value"
	# 	- Get cards with highest count 
	#	- sort suits by whichever comes first
	# 	- change wild_card to that suite
	top_suits = wild_card
	top_suits_by_count = [ x[0] for x in card_counts if x[1] == card_counts[0][1] and x[0] != wild_card ]
	top_suit_index = len(cards)-1
	for suite in top_suits_by_count:
		top_suit_index = cards.index(suite) if cards.index(suite) <= top_suit_index else top_suit_index

	if len(card_counts) == 1:
		replacement = deck.unique_cards[-1]
	else:
		if wild_card_i < top_suit_index:
			replacement = largest_non_wild
		else:
			replacement = cards[top_suit_index]

	new_cards = cards.replace(wild_card, replacement)
	
	if debug_hand: logging.debug('\t\t\t' + f'---: {cards}>>{new_cards}')

	return new_cards

def hand_scoring(cards, deck, debug_hand=False):
	previous_logging_level = logging.root.level
	logging.getLogger().setLevel(logging.DEBUG)

	card_counts = count_cards(cards, deck) # sorted
	if debug_hand: logging.debug('\t' + f'----- CARD COUNTS: {card_counts}')

	sub_score = hand_subscoring(cards, deck, debug_hand)

	card_counts = [ x[1] for x in card_counts ]
	hand_scores = [
		card_counts[0] == 5,
		card_counts[0] == 4, 
		card_counts[0] == 3 and card_counts[1] == 2,
		card_counts[0] == 3, 
		card_counts[0] == 2 and card_counts[1] == 2,
		card_counts[0] == 2,
		True,
	]
	hand_scores_str = [ 
		'Five of a kind',
		'Four of a kind',
		'Full House',
		'Three of a kind',
		'Two Pair',
		'One Pair',
		'High Card',
	]
	
	# logging.debug('\t' + f'{hand_scores=}')
	result = hand_scores.index(True)
	
	hand_score_str = hand_scores_str[result]
	hand_score = len(hand_scores) - hand_scores.index(True) -1
	hand_score_rebase = hand_score * deck.base ** len(cards)
	if debug_hand: 
		logging.debug('\t' + f'{hand_score_str=} :: {hand_score}*{deck.base ** len(cards):,}={hand_score_rebase:,}')
		logging.debug('\t' + f'{sub_score=}')

	logging.getLogger().setLevel(previous_logging_level)
	return hand_score_str, hand_score_rebase, sub_score 

def betting(problem_num, hands_to_debug=0, debug_criteria = lambda hand:True):
	with open(input_file,'r') as f:
		players = [x.split() for x in f.read().split('\n')]
	
	# unique_cards = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
	unique_cards = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
	deck = deck_class(unique_cards)

	h_count = 0
	player_num = 0
	for player in players:
		hand = player[0]
		bid = player[1]
		player_num += 1

		h_count += 1 if debug_criteria(hand) else 0
		debug_hand = debug_criteria(hand) and h_count<=hands_to_debug

		if debug_hand:logging.debug(f'Debug #{h_count}--Player {player_num}: {hand}')
		hand_score_str, score_pairs, score_sub = hand_scoring(hand,deck,debug_hand)
		hand_base= [hand_score_str, hand, score_sub+score_pairs,score_sub ]

		hand_changed=[hand_score_str,'no change',score_pairs+score_sub, score_sub ]
		if problem_num==2: 
			card_counts = count_cards(hand,deck)
			new_cards = handle_wild_card(hand,card_counts,deck, debug_hand)
			card_counts = count_cards(new_cards,deck)

			if debug_hand: logging.debug('\t' + f'----- CARD COUNTS: {new_cards}')
			hand_score_str, score_pairs, score_sub  = hand_scoring(new_cards,deck,debug_hand)
			hand_changed = [hand_score_str,new_cards,score_pairs+score_sub, score_sub]

		player.insert(0,f'Player {player_num}')
		player[1] = hand_base
		player.insert(2,hand_changed)
		player[-1] = int(player[-1])
		
	# Sort on total score of the Changed hand first - THEN sort on the sub-score of the hand before it was changed (if there is a tie)
	players.sort(key=lambda x:(x[2][2], x[1][3]))
	logging.debug(pprint.pformat([x for x in players if x[1][0] == "Two Pair" and 'J' in x[1][1] and x[1][1].count('J') == 1],indent=4))
	# logging.debug(pprint.pformat(players))
	total_winnings = 0
	for p in range(len(players)):
		total_winnings += players[p][3] * (p+1)
	logging.info(f'  --Answer: {total_winnings} (pretty: {total_winnings:,})')  

def handler():
	problems = {
		'1' : lambda: betting(problem_num=1), # Answer is: 249,204,891
		'2' : lambda: betting(problem_num=2, hands_to_debug=1000, debug_criteria=lambda hand: 'J' in hand) 
		# answer: 249,275,219 too low
		# answer: 249,416,323 too low
		# answer: 249,695,034 NOT correct
		# answer: 252,239,451 too high
	}
	for prb_num, prb in problems.items():
		start_time = time.time()
		logging.info(f' day {day}, problem {prb_num} '.center(padding_size_large,padding_char))
		prb()
		logging.debug(f' --runtime= {datetime.timedelta(seconds=time.time() - start_time)}')


handler()
