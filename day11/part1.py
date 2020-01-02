
import logging
import sys
sys.path.insert(0, '..')
from typing import List
from collections import defaultdict
from intcode import IntcodeComputer, read_input


logging.basicConfig(level=logging.INFO)


_INPUT_FILE='input.txt'


class PaintingRobot:
    """ Executes the given intcode program, painting tiles based on its output"""

    def __init__(self, intcode: List[int]):
        self.intcode = intcode
        self.current_position = (0, 0)
        self.orientation = (0, 1)
        self.painting_area = defaultdict(int)
        self.intcode_computer = IntcodeComputer(intcode, self.get_input, self.generate_output)
        self.waiting_for_direction = False
    
    def get_input(self):
        logging.info(f"Reading tile {self.current_position} with color {self.painting_area[self.current_position]}")
        return self.painting_area[self.current_position]
    
    def generate_output(self, x: int):
        if self.waiting_for_direction:
            if x == 0:
                # Turn left 90 degrees
                if self.orientation == (0,1):
                    self.orientation = (-1, 0)
                elif self.orientation == (-1,0):
                    self.orientation = (0,-1)
                elif self.orientation == (0,-1):
                    self.orientation = (1, 0)
                elif self.orientation == (1,0):
                    self.orientation = (0, 1)
            else:
                if self.orientation == (0,1):
                    self.orientation = (1, 0)
                elif self.orientation == (-1,0):
                    self.orientation = (0,1)
                elif self.orientation == (0,-1):
                    self.orientation = (-1, 0)
                elif self.orientation == (1,0):
                    self.orientation = (0, -1)
            self.current_position = (self.current_position[0] + self.orientation[0], self.current_position[1] + self.orientation[1])
            self.waiting_for_direction = False
            logging.info(f"Updated orientation to  {self.orientation} and position to  {self.current_position}")
        else:
            logging.info(f"Painting {self.current_position} with {x}")
            self.painting_area[self.current_position] = x
            self.waiting_for_direction = True
    
    def execute(self):
        self.intcode_computer.execute()


def main(intcode: List[int] = None):
    if not intcode:
        intcode = read_input(input_file=_INPUT_FILE)
    pr = PaintingRobot(intcode)
    pr.execute()
    return len(pr.painting_area.keys())


if __name__ == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        intcode = [int(n) for n in sys.argv[1].split(",")]
    print(f"tiles painted: {main(intcode)}")