import sys
sys.path.insert(0, '..')

import logging
logging.basicConfig(level=logging.WARNING)

import os
import numpy as np
from typing import List, Set
from collections import defaultdict, namedtuple
from intcode import IntcodeComputer, read_input


Pos = namedtuple('Pos', ['x', 'y'])


_INPUT_FILE='input.txt'


class Drone:
    """ Executes the given intcode program, to play a game"""

    def __init__(self, intcode: List[int]):
        self.intcode = intcode
        self.current_position = (0, 0)
        self.search_space = defaultdict(int)
        self.search_space[self.current_position] = -1
        self.unvisited_nodes = set()
        self.explored = defaultdict(int)
        self.solution_path = []
        self.image = None
        self.intcode_computer = IntcodeComputer(intcode, self.get_input, self.generate_output)
        self.moves = {1: (0,1), 2:(0,-1), 4:(1,0), 3:(-1,0)}

    def get_input(self):
        return self.input
    
    def generate_output(self, value: int):
        print(f"Got {value}")
        temptative_positon = self.next_position(self.input)
        self.search_space[temptative_positon] = value
        if value != 0:
            self.current_position = temptative_positon

    def execute(self):
        while self.intcode_computer.has_next():
            next(self.intcode_computer.process_intcode())
    
    def next_position(self, mov) -> Pos:
        if mov == 1:
            return (self.current_position[0], self.current_position[1] +1)
        elif mov == 2:
            return (self.current_position[0], self.current_position[1] -1)
        elif mov == 3:
            return (self.current_position[0] + 1, self.current_position[1])
        elif mov == 4:
            return (self.current_position[0] - 1, self.current_position[1])

    def step_back(self):
        # Remove step from solution path
        print(f"Found dead end, stepping back from {self.current_position}")
        last_move = self.solution_path.pop()
        # Undo step
        if last_move == 1:
            self.input = 2
        elif last_move == 2:
            self.input = 1
        elif last_move == 3:
            self.input = 4
        elif last_move == 4:
            self.input = 3
        self.intcode_computer.step()

    def step_forward(self, mov) -> bool:
        self.input = mov
        self.solution_path.append(mov)
        self.intcode_computer.step()

    def explore(self, mov, next_pos):
        print(f"Trying {mov} from {self.current_position}")
        self.step_forward(mov)
        if self.search_space[next_pos] == 2:
            print(f"Solution found at {next_pos} in {len(self.solution_path)} steps")
            print(self.solution_path)
            self.display_screen()
            return True
        elif self.search_space[next_pos] == 0:
            # Hit a wall, remove step from solution path
            self.solution_path.pop()
            return False
        else:
            self.explored[self.current_position] = 1
            for mov in self.moves.keys():
                next_pos = self.next_position(mov)
                if self.explored[next_pos] == 0:
                    found = self.explore(mov, next_pos)
                    if found:
                        return True
            self.step_back()
            return False

    def command_line_display(self, image):
        for x in range(image.shape[0]):
            string = []
            for y in range(image.shape[1]):
                if image[x,y] == -1:
                    string.append('@')
                if image[x,y] == 0:
                    string.append('#')
                if image[x,y] == 1:
                    string.append('X')
                if image[x,y] == 2:
                    string.append('*')
                if image[x,y] == 3:
                    string.append('.')
            print(''.join(string))

    def display_screen(self):
        # if self.image is None:
        self.min_x = min(key[0] for key in self.search_space.keys())
        max_x = max(key[0] for key in self.search_space.keys())
        min_y = min(key[1] for key in self.search_space.keys())
        self.max_y = max(key[1] for key in self.search_space.keys())

        size_x = max_x - self.min_x
        size_y = self.max_y - min_y

        self.image = np.ones(shape=(size_y + 1, size_x + 1)) * 3
        for position,color in self.search_space.items():
            # Correct coordinates. In the array (0,0) is top left
            if position == (0,0): color = -1
            self.image[abs(position[1] - self.max_y), abs(position[0] - self.min_x)] = color
        self.command_line_display(self.image)


def main(intcode: List[int] = None):
    if not intcode:
        intcode = read_input(input_file=_INPUT_FILE)
    drone = Drone(intcode)
    for i in range(1,5):
        result = drone.explore(i, (0,0))
        if result:
            return


if __name__ == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        intcode = [int(n) for n in sys.argv[1].split(",")]
    main(intcode)