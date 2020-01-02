
import logging
import sys
sys.path.insert(0, '..')
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple
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
        self.painting_area[self.current_position] = 1
        self.intcode_computer = IntcodeComputer(intcode, self.get_input, self.generate_output)
        self.waiting_for_direction = False
    
    def get_input(self):
        logging.info(f"Reading tile {self.current_position} with color {self.painting_area[self.current_position]}")
        return self.painting_area[self.current_position]
    
    def update_orientation(self, turn_to: int):
        x, y = self.orientation
        # Change sign if x=0 and have to turn left, or if x=1 and have to turn right
        sign = -1 if abs(x) == turn_to else 1
        self.orientation = (sign * y, sign * x)
    
    def generate_output(self, value: int):
        if self.waiting_for_direction:
            self.update_orientation(value)
            ox, oy, x, y = (*self.orientation, *self.current_position)
            self.current_position = (x + ox, y + oy)
            self.waiting_for_direction = False
            logging.info(f"Updated orientation to  {self.orientation} and position to  {self.current_position}")
        else:
            logging.info(f"Painting {self.current_position} with {value}")
            self.painting_area[self.current_position] = value
            self.waiting_for_direction = True
    
    def execute(self):
        self.intcode_computer.execute()


def paint_registration_id(painting_area: Dict[Tuple[int,int], int]):
    min_x = min(key[0] for key in painting_area.keys())
    max_x = max(key[0] for key in painting_area.keys())
    min_y = min(key[1] for key in painting_area.keys())
    max_y = max(key[1] for key in painting_area.keys())

    size_x = max_x - min_x
    size_y = max_y - min_y

    image = np.zeros(shape=(size_y + 1, size_x + 1))
    for position,color in painting_area.items():
        # Correct coordinates. In the array (0,0) is top left
        image[abs(position[1] - max_y), abs(position[0] - min_x)] = color
    plt.imshow(image, cmap="gray")
    plt.show()


def main(intcode: List[int] = None):
    if not intcode:
        intcode = read_input(input_file=_INPUT_FILE)
    pr = PaintingRobot(intcode)
    pr.execute()
    paint_registration_id(pr.painting_area)
    return pr.painting_area


if __name__ == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        intcode = [int(n) for n in sys.argv[1].split(",")]
    main(intcode)