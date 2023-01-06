import os
import logging
logging.basicConfig(level=logging.INFO)
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day_02_input.txt'

def day_02_prb_1():
	logging.info('day 2, problem 1')
	score = 0
	with open(input_file,'r') as f:
		lines = f.readlines()
		logging.debug(f'{lines=}')
		for line in lines:
			raw_move_elf, raw_move_me = line.split()
			
			move_elf = ['A','B','C'].index(raw_move_elf)
			move_me = ['X','Y','Z'].index(raw_move_me)

			pretty_moves = ['Rock','Paper','Scissors']
			logging.debug(f'My move: {pretty_moves[move_me]}, Elf Move: {pretty_moves[move_elf]}')

			# Shape Score
			score += move_me + 1

			# 0 = Rock
			# 1 = Paper
			# 2 = Scissors
			if move_elf == move_me:
				score += 3
				logging.debug('\t TIE')
			elif move_me-move_elf == 1 or move_me-move_elf == -2: # win
				score += 6
				logging.debug('\t WIN')
			else:
				logging.debug('\t LOSE')
		
	print(f'{score=}')

def day_02_prb_2():
	logging.info('day 2, problem 2')
	score = 0
	with open(input_file,'r') as f:
		lines = f.readlines()
		logging.debug(f'{lines=}')
		for count, line in enumerate(lines):
			raw_move_elf, raw_outcome = line.split()

			pretty_moves = ['Rock','Paper','Scissors']
			pretty_outcomes = ['Lose', 'Tie','Win']
			
			move_elf = ['A','B','C'].index(raw_move_elf)
			pretty_outcome = pretty_outcomes[['X','Y','Z'].index(raw_outcome)]
			
			if pretty_outcome == 'Tie':
				outcome_score = 3 
				my_move = move_elf
			elif pretty_outcome == 'Win':
				outcome_score = 6
				my_move = (move_elf + 1) % 3
			else:
				outcome_score = 0
				my_move = (move_elf - 1) % 3
			shape_score = my_move + 1
			score += shape_score + outcome_score
			logging.debug(f'Line {count}--- {raw_move_elf}={pretty_moves[move_elf]}, {raw_outcome}={pretty_outcome}({outcome_score}) with {pretty_moves[my_move]}({shape_score})')
	print(f'{score=}')


if __name__ == '__main__':
	day_02_prb_1() # Answer = 12645
	day_02_prb_2() # Answer = 11756