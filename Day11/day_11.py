import os

import re
import json
import time
import datetime
import logging

logging.basicConfig(level=logging.INFO)
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file = file_path + 'day_11_input.txt'

'''
Assumptions: 
- Monkey names are just their index in a list of monkeys (starts at indx=0)
- no leading empty-line in the input
- only one empty line between Monkey inputs
'''
class Monkey ():
    def __init__(self, items, operation_str, test_str, test_denominator, if_true_throw_to, if_false_throw_to, inspection_count=0):
        self.items = items
        self.operation = None
        self.operation_str = operation_str
        self.test = None
        self.test_str = test_str
        self.test_denominator = test_denominator
        self.if_true_throw_to = if_true_throw_to
        self.if_false_throw_to = if_false_throw_to
        self.inspection_count = inspection_count
    
    def to_string(self):
        s = '\n\t' + f'{self.items=}'
        s += '\n\t' + f'{self.operation_str=}'
        s += '\n\t' + f'\tExample OPERATION w/Old= 5: {self.operation(5)}'
        s += '\n\t' + f'{self.test_str=}'
        s += '\n\t' + f'\tExample TEST w/num = 323: {self.test(323)}'
        s += '\n\t' + f'\tdenominator: {self.test_denominator}'
        s += '\n\t' + f'{self.if_true_throw_to=}'
        s += '\n\t' + f'{self.if_false_throw_to=}'
        s += '\n\t' + f'{self.inspection_count=}'
        return s

def print_monkeys(monkeys):
    for i, monkey in enumerate(monkeys):
        logging.debug(f'Monkey {i}')
        logging.debug('\t' + monkey.to_string() + '\n')

def input_to_monkeys(data):
    monkeys = []
    current_monkey = 0
    starting_items = []
    operation_str = ''
    test_str = ''
    if_true = ''
    if_false = ''

    for l in data:
        logging.debug(l)
        if l != '':
            command, value = l.split(':')
            command = command.strip()
            value = value.strip()
            if command[:6] == "Monkey":
                # Ex: "Monkey 2:" == "2"
                current_monkey = int(command.split()[1])
            elif command == "Starting items":
                starting_items = list(map(int, value.strip().split(', ')))
            elif command == "Operation":
                operation_str = 'new_monkey.operation = lambda old: ' + value[len('new = '):]
            elif command == "Test":
                denominator = int(value.strip()[len('divisible by '):])
                test_str = f'new_monkey.test = lambda x: x%{denominator} == 0'
            elif command == "If true":
                if_true = int(value.strip()[len('throw to monkey '):])
            elif command == "If false":
                if_false = int(value.strip()[len('throw to monkey '):])
        else: 
            new_monkey = Monkey(
                starting_items.copy(),
                operation_str,
                test_str,
                denominator,
                if_true,
                if_false
            )
            exec(test_str)
            exec(operation_str)
            monkeys.append(new_monkey)
    new_monkey = Monkey(
            starting_items.copy(),
            operation_str,
            test_str,
            denominator,
            if_true,
            if_false
    )
    exec(test_str)
    exec(operation_str)
    monkeys.append(new_monkey)

    return monkeys

def day_11_prb_1():
    print('-'*50)
    print('day 11, problem 1')

    with open(input_file,'r') as f:
        data = f.read().splitlines()
        monkeys = input_to_monkeys(data)
        print_monkeys(monkeys)
        logging.debug('-'*20)

        round = 0
        round_limit = 20
        print_round_details = False

        for round in range(1, round_limit+1):
            logging.debug('-'*50)
            logging.debug(f'Round: {round}')

            for i, m in enumerate(monkeys):
                if print_round_details:
                    logging.debug(f'MONKEY: {i}' + '-'*20)
                    logging.debug(f'operation:{m.operation_str}')
                    logging.debug(f'test:{m.test_str}')
                for item in m.items:
                    inspect_worry = m.operation(item)
                    bored_worry = inspect_worry//3
                    test = m.test(bored_worry)

                    if test:
                        test_result_action = f'\t\t    Throw to monkey {m.if_true_throw_to}'
                        monkeys[m.if_true_throw_to].items.append(bored_worry)
                        m.items = m.items[1:]
                    else: # false
                        test_result_action = f'\t\t    Throw to monkey {m.if_false_throw_to}'
                        monkeys[m.if_false_throw_to].items.append(bored_worry)
                        m.items = m.items[1:]
                    
                    if print_round_details:
                        logging.debug(f'\tItem: {item} worry')
                        logging.debug(f'\t\tAfter Inspected: {inspect_worry}')
                        logging.debug(f'\t\tBored (/3): {bored_worry}')
                        logging.debug(f'\t\tDivisible?: {test}')
                        logging.debug(test_result_action)

                    m.inspection_count += 1

            logging.debug('-'*50)
            logging.debug(''.join([ f'\nMonkey {i}: items: '+str(m.items) + f'\n    inspected: {m.inspection_count}' for i,m in enumerate(monkeys)]))
            logging.debug(f'\tTOTAL ITEMS: {sum( len(m.items) for m in monkeys )}')

    logging.debug('-'*50)
    print(''.join([ f'\nMonkey {i}: \n    items: '+str(m.items) + f'\n    inspected: {m.inspection_count}' for i,m in enumerate(monkeys)]))
    inspection_counts = [ m.inspection_count for m in monkeys ]
    inspection_counts.sort(reverse=True)
    print(f'Top two inspections: {inspection_counts[:2]}')
    print(f'Answer: {inspection_counts[0] * inspection_counts[1] }')

# Source:
# https://stackoverflow.com/questions/37237954/calculate-the-lcm-of-a-list-of-given-numbers-in-python
from math import gcd
# PROCESS:
#   1. find the Least Common Denominator, lcd, between the first two numbers
#   2. since that is the lcd, it's the LOWEST you can go and all future lcd's 
#           need to use that as a base 
#   3. you then find the lcd between the previous lcd and the next number
#   4. continue until done
def lcd(a):
    lcm = 1
    for i in a:
        lcm = lcm*i//gcd(lcm, i)
    return lcm

def day_11_prb_2():
    start_time = time.time()
    print('-'*50)
    print('day 11, problem 2')

    with open(input_file,'r') as f:
        data = f.read().splitlines()
        monkeys = input_to_monkeys(data)
        # print_monkeys(monkeys)

        # to keep numbers small, we find the least common denominator 
        # among testing algorithms, which will be used to find the remainder 
        # of altered "worry" of items but still allow for accurate testing
        least_common_denominator = lcd([ m.test_denominator for m in monkeys ])
        print(f'{least_common_denominator=}')
        logging.debug('-'*20)

        round = 0
        round_limit = 10000
        print_round_details = False
        print_rounds = [1, 20] +  list(range(1000,10000,1000))

        for round in range(1, round_limit+1):
            if print_rounds is None or round in print_rounds:
                logging.debug('-'*50)
                logging.debug(f'Round: {round}')
            else: 
                print(f'Round: {round}', end='\r')

            for i, m in enumerate(monkeys):
                if print_round_details:
                    logging.debug(f'MONKEY: {i}' + '-'*20)
                    logging.debug(f'operation:{m.operation_str}')
                    logging.debug(f'test:{m.test_str}')
                
                for item in m.items:
                    inspect_worry = m.operation(item)
                    
                    test = m.test(inspect_worry)
                    lcd_worry = inspect_worry%least_common_denominator

                    if test:
                        test_result_action = f'\t\t    Throw to monkey {m.if_true_throw_to}'
                        monkeys[m.if_true_throw_to].items.append(lcd_worry)
                        m.items = m.items[1:]
                    else: # false
                        test_result_action = f'\t\t    Throw to monkey {m.if_false_throw_to}'
                        monkeys[m.if_false_throw_to].items.append(lcd_worry)
                        m.items = m.items[1:]
                    
                    if print_round_details:
                        logging.debug(f'\tItem: {item} worry')
                        logging.debug(f'\t\tAfter Inspected: {lcd_worry}')
                        logging.debug(f'\t\tDivisible?: {test}')
                        logging.debug(test_result_action)
                        logging.debug(f'\tMonkey {i}--total items inspected: {sum( len(m.items) for m in monkeys )}')
                        
                    m.inspection_count += 1
            if print_rounds is None or round in print_rounds:
                logging.debug(f'Processing time: {datetime.timedelta(seconds=time.time() - start_time)}')
                # logging.debug('-'*50)
                logging.debug(''.join([ f'\nMonkey {i}: total inspected: {m.inspection_count}' for i,m in enumerate(monkeys)]))
                # logging.debug(f'\ttotal items inspected: {sum( len(m.items) for m in monkeys )}')

    logging.debug('-'*50)
    print(''.join([ f'\nMonkey {i}: \n    items: '+str(m.items) + f'\n    inspected: {m.inspection_count}' for i,m in enumerate(monkeys)]))
    inspection_counts = [ m.inspection_count for m in monkeys ]
    inspection_counts.sort(reverse=True)
    print(f'Top two inspections: {inspection_counts[:2]}')
    print(f'Answer: {inspection_counts[0] * inspection_counts[1] }')

if __name__ == '__main__':
	day_11_prb_1() # Answer is 99852
	day_11_prb_2() # Answer is 25935263541