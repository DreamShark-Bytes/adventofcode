import os
import re
import logging


logging.basicConfig(level=logging.DEBUG)


'''
ASSUMPTIONS (from input data):
- exactly 2 lines and an empty line between various pairs of lines
- no spaces
- bracketed lists always have matching brackets
- lists have appropriate commas
- list values are only numbers or other lists
- numbers can be MULTIPLE digits
'''


file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day_13_input.txt'
padding_size_large = 100
padding_size = 80
padding_char = '-'

def str_to_lists(my_str):
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.INFO)
    indent='\t'

    output = []
    level = 1
    current_level = 0
    prev_comma=0
    i = 0
    for char in my_str:
        logging.debug(f'{indent}{char=}, {current_level=}')
        
        if current_level == level and (char==',' or char==']'):
            logging.debug(f'{indent*2}{prev_comma=},{i=}')
            temp_str = my_str[prev_comma+1:i]
            logging.debug(f'{indent*2}{temp_str=}')
            prev_comma = i
            if re.fullmatch('[0-9]+',temp_str):
                output.append(int(temp_str))
            elif temp_str != '': 
                output.append(str_to_lists(temp_str))
        if char == '[':
            current_level += 1
        elif char == ']':
            current_level -= 1
        i += 1
        
    logging.debug(f'{indent}{output=}')
    logging.getLogger().setLevel(previous_logging_level)
    return output

# Output = True if the Left and Right lists are "In the Right Order"
def left_vs_right(left_list, right_list, depth=1):
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.INFO)
    indent = '|   '
    in_order = None
    l = len(left_list)
    r = len(right_list)

    for i in range(max(l,r)):
        if i > l-1 and i <= r-1: 
            logging.debug(f'{indent*depth}✔️  RIGHT order: Left is SHORTER than Right')
            return True
        elif i <= l-1 and i > r-1: 
            logging.debug(f'{indent*depth}❌ WRONG order: Left is LONGER than Right')
            return False

        left_item = left_list[i]
        right_item = right_list[i]

        if type(left_item) is list or type(right_item) is list: 
            if type(right_item) is not list:
                in_order = left_vs_right(left_item, [right_item],depth=depth+1)
            elif type(left_item) is not list:
                in_order = left_vs_right([left_item], right_item,depth=depth+1)
            else:
                in_order = left_vs_right(left_item, right_item,depth=depth+1)
            if in_order is not None: return in_order
        else:
            logging.debug(f'{indent*depth}Comparing: {left_item} vs {right_item}')
            if left_item < right_item:
                logging.debug(f'{indent*depth}✔️  RIGHT order: Left is LESS than Right')
                return True
            elif left_item > right_item:
                logging.debug(f'{indent*depth}❌ WRONG order: Left is BIGGER than Right')
                return False
    logging.getLogger().setLevel(previous_logging_level)
        

def day_13_prb_1():
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.INFO)
    logging.info(' day 13, problem 1 '.center(padding_size_large,padding_char))

    pair_results = []
    with open(input_file,'r') as f:
        data = f.read().splitlines()
        for di in range(0,len(data),3):
            s = f'PAIR {di//3+1}'.center(30,'-')
            logging.debug(s)
            left = data[di]
            right = data[di+1]
            # empty_line = data[di+2]

            logging.debug(f'LEFT (line1)="{left}"')
            left = str_to_lists(left)
            logging.debug(f'RIGHT (line2)="{right}"')
            right = str_to_lists(right)

            # logging.debug(f'\tconverted={left}')
            # logging.debug(f'\tconverted={right}')

            outcome = left_vs_right(left, right)
            pair_results.append(outcome)
            logging.debug(f'OUTCOME: {outcome}')

    scores = [ pi+1 if pair_results[pi] else 0 for pi in range(len(pair_results)) ]

    pretty_pairs = [ f'p{str(i)}:✔️ :{str(scores[i])}' if pair_results[i] else f'p{str(i)}:❌:0' for i in range(len(pair_results)) ]
    logging.info( 'Pair Results and scores = ' + ', '.join(pretty_pairs))
    
    # pretty_scores = [ str(s).rjust(3) for s in scores ]
    # logging.info(f'      Scores ={ "".join(pretty_scores)}')
    logging.info(f'{sum(scores)=}')
    logging.getLogger().setLevel(previous_logging_level)

def day_13_prb_2():
    previous_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info(' day 13, problem 2 '.center(padding_size_large,padding_char))

    packets_processed = []
    pair_results = []
    with open(input_file,'r') as f:
        data = f.read().splitlines()
        for di in range(0,len(data)):
            if data[di] == '': continue

            packet = data[di]
            packet = str_to_lists(packet)
            packets_processed.append(packet.copy())

            # outcome = left_vs_right(left, right)
    # Add the divider packets into the fray
    dividers = [
        [[2]],
        [[6]]
    ]
    for d in dividers:
        packets_processed.append(d)
    
    # What ever, brute force it BABY
    sort_scores = [
        sum( [
            1
            if left_vs_right(left_packet, right_packet)
            else
            0 
            for right_packet in packets_processed
        ])
        for left_packet in packets_processed
    ]
    packets_scored = list(zip(sort_scores, packets_processed))
    packets_scored.sort(key=lambda x: x[0],reverse=True)
    for score, ps in packets_scored[:10]:
        logging.debug(f'{score=}, {ps=}')
    
    only_packets_sorted = [ p[1] for p in packets_scored ]
    decoder_key = 1
    for d in dividers:
        i = only_packets_sorted.index(d)+1
        logging.debug(f'Divider {d}, found at sport: {i}')
        decoder_key *= i

    logging.info(f'FINISHED-- {decoder_key=}')
    logging.getLogger().setLevel(previous_logging_level)
    

if __name__ == '__main__':
    day_13_prb_1() # Answer is 5659
    day_13_prb_2() # Answer is 22110