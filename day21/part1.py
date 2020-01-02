import numpy as np
import sys
sys.path.insert(0, '/home/chema/advent-of-code-2019/')
import os
import logging
logging.basicConfig(level=logging.WARNING)
import time
from typing import List, Set, Tuple, Dict
from collections import defaultdict, namedtuple
from intcode import IntcodeComputer, read_input
import curses
import copy

Pos = namedtuple('Pos', ['x', 'y'])

logging.basicConfig(level=logging.INFO)

_INPUT_FILE='input.txt'


class SpringDroid:
    """ Executes the given intcode program, to navigate through damaged hull"""

    def __init__(self, intcode: List[int]):
        self.intcode = intcode
        # Jum if :
        #   - 4 is ground
        #   - AND (1 empty or 2 empty or 3 empty)
        self.program = ['NOT A T','NOT B J','OR J T','NOT C J','OR T J', 'AND D J', 'WALK']
        self.result = []
        self.instructions = (ascii_char for line in self.program for ascii_char in self.to_ascii(line) )

    def to_ascii(self, instruction: str) -> List[int]:
        ascii_instruction = [ord(char) for char in instruction]
        return ascii_instruction + [10]

    def get_input(self):
        return next(self.instructions)

    def generate_output(self, value: int):
        try :
            self.result.append(chr(value))
        except:
            self.result.append(str(value))
    
    def execute(self):
        self.intcode_computer = IntcodeComputer(self.intcode, self.get_input, self.generate_output)
        while self.intcode_computer.has_next():
            next(self.intcode_computer.process_intcode())


def main(intcode: List[int] = None):
    if not intcode:
        intcode = read_input(input_file=_INPUT_FILE)
    droid = SpringDroid(intcode)
    droid.execute()
    print(''.join(droid.result))


if __name__ == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        intcode = [int(n) for n in sys.argv[1].split(",")]
    main(intcode)