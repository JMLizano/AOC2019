import logging
logging.basicConfig(level=logging.WARNING)

import sys
sys.path.insert(0, '..')

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple
from collections import defaultdict, namedtuple
from intcode import IntcodeComputer, read_input


logging.basicConfig(level=logging.WARNING)


_INPUT_FILE='input.txt'


class Arcade:
    """ Executes the given intcode program, to play a game"""

    def __init__(self, intcode: List[int]):
        self.intcode = intcode
        self.current_position = (0, 0)
        self.screen = defaultdict(int)
        self.intcode_computer = IntcodeComputer(intcode, self.get_input, self.generate_output)
        self.offset = 0
        self.score = 0 
    
    def get_input(self):
        return 0
    
    def generate_output(self, value: int):
        if self.offset == 0:
            self.x = value
            self.offset += 1
        elif self.offset == 1:
            self.y = value
            self.offset += 1
        elif self.offset == 2:
            if self.x == -1 and self.y == 0:
                logging.warning(f"Setting score to {value}")
                self.score = value
            else:
                logging.warning(f"Setting tile in {self.x},{self.y} with {value}")
                self.screen[(self.x,self.y)] = value
            self.offset = 0  
    
    def execute(self):
        self.intcode_computer.execute()


def main(intcode: List[int] = None):
    if not intcode:
        intcode = read_input(input_file=_INPUT_FILE)
    arc = Arcade(intcode)
    arc.execute()
    print()
    print(sum(1 for x in arc.screen.values() if x == 2))


if __name__ == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        intcode = [int(n) for n in sys.argv[1].split(",")]
    main(intcode)