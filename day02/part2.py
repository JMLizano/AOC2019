import sys
import logging
from typing import List
from part1 import read_input, process_intcode_operation


logging.basicConfig(level=logging.INFO)


_INPUT_FILE = 'input.txt'


def find_noun_verb_for_value(value:int) -> List[int]:
    for n in range(100):
        for v in range(100):
            logging.info("Trying noun {} and verb {}".format(n,v))
            intcode = read_input(input_file=_INPUT_FILE)
            intcode[1] = n
            intcode[2] = v
            intcode = process_intcode_with_condition(intcode, value)
            if intcode[0] == value:
                logging.info("Found noun {} and verb {} for value {}".format(n,v, intcode[0]))
                return n,v


def process_intcode_with_condition(intcode: List[int], value: int) -> List[int]:
    current_pos = 0
    opcode = None
    while(current_pos < len(intcode) and opcode != 99):
        intcode, opcode = process_intcode_operation(intcode, current_pos)
        if intcode[0] > value:
            break
        current_pos += 4
    return intcode


if __name__  == '__main__':
    value = 19690720
    if len(sys.argv) > 1:
        value = int(sys.argv[1])
    noun, verb = find_noun_verb_for_value(value)
    print(f"Verb: {verb}, Noun: {noun}. Operation: {100 * noun + verb}")