import os
import logging
import time
import re
# logging.basicConfig(level=logging.DEBUG)
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day_01_input.txt'
padding_size_large = 100
padding_size_medium = 45
padding_char = '-'

def decipher_line(line):
	first_found = False
	last_digit_found = '0'
	digit = ''
	for char in line:
		if char.isnumeric():
			last_digit_found = char
			if not first_found:
				first_found = True
				digit += char
	digit += last_digit_found
	return int(digit)

def decipher_simple(lines, lines_to_debug=0):
	lines_read = 0;
	
	total = 0;
	for line in lines:
		lines_read += 1
		
		num = decipher_line(line)
		if lines_read <= lines_to_debug:
			logging.debug(f'Line {lines_read}: "{line}"')
			logging.debug(f'\t-Digits found: {num}')
		total += num
	logging.info(f'Answer: {total}');

def decipher_complex(lines,lines_to_debug=0):
	number_words = {
		'zero':'0',
		'one':'1',
		'two':'2',
		'three':'3',
		'four':'4',
		'five':'5',
		'six':'6',
		'seven':'7',
		'eight':'8',
		'nine':'9'
	}
	total = 0
	for i in range(len(lines)):
		line = lines[i]
		found_digits = ''
		
		new_line = ''
		char_pos = 0
		while char_pos < len(line):
			digit_found = False
			for k,v in number_words.items():
				if line[char_pos:].startswith(k):
					found_digits+=v
					new_line += v
					digit_found = True
					break;
			if not digit_found:
				new_line += line[char_pos]
			char_pos +=1
		dl = decipher_line(new_line)
		total += dl
		if i < 	lines_to_debug:
			logging.debug(f'Line {i+1}: "{line}"')
			logging.debug(f'\t-Digits found: {found_digits}')
			logging.debug(f'\t-{new_line=}')
			logging.debug(f'\t-Deciphered: {dl}')
		lines[i] = new_line
	logging.info(f'Answer: {total}');

def handler():
	logging.getLogger().setLevel(logging.DEBUG)
	lines_to_debug = 5
	
	with open(input_file,'r') as f:
		lines = f.read().split()

	logging.info(' day 1, problem 1 '.center(padding_size_large,padding_char))
	decipher_simple(lines, lines_to_debug=0)
	
	logging.info(' day 1, problem 2 '.center(padding_size_large,padding_char))
	decipher_complex(lines, lines_to_debug=0)
	
handler()