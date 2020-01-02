import numpy as np
import sys
sys.path.insert(0, '/home/chema/advent-of-code-2019/')
import os
import logging
logging.basicConfig(level=logging.WARNING)
import time
from typing import List, Set
from collections import defaultdict, namedtuple
from intcode import IntcodeComputer, read_input
import curses
import copy

Pos = namedtuple('Pos', ['x', 'y'])

logging.basicConfig(level=logging.INFO)

_INPUT_FILE='input.txt'


class Drone:
    """ Executes the given intcode program, to play a game"""

    def __init__(self, intcode: List[int]):
        self.intcode = intcode
        self.x = NotImplemented
        self.y = None
        self.give_x = True
        self.scanning = (None,None)
        self.current_position = (self.x, self.y)
        self.tractor_area = defaultdict(int)
        self.moves = {1: (0,1), 2:(0,-1), 4:(1,0), 3:(-1,0)}
        self.input_x = (x for point in zip(range(50), range(50)) for x in point)

    def get_input(self):
        print(f"Giving {self.x, self.y}") 
        if self.give_x:
            self.give_x = False
            return self.x
        else:
            self.give_x = True
            return self.y
    
    def generate_output(self, value: int):
        print(f"Got {value} on {self.x, self.y}")
        self.tractor_area[(self.x, self.y)] = value
    
    def execute(self):
        self.intcode_computer = IntcodeComputer(self.intcode, self.get_input, self.generate_output)
        while self.intcode_computer.has_next():
            next(self.intcode_computer.process_intcode())
    
    def execute_for_grid(self, max_x: int, max_y: int):
        for y in range(max_y):
            self.y = y
            for x in range(max_x):
                self.x = x
                self.execute()
    
    def curses_display(self, stdscr):
        stdscr.clear()
        stdscr.refresh()
        x,y = zip(*self.tractor_area.keys())
        xmin, xmax = min(x), max(x)
        ymin, ymax = min(y), max(y)
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                block = self.tractor_area[(x,y)]
                character = "#" if block == 0 else "."
                stdscr.addstr(abs(x - xmin),abs(y - ymin), character) 
                stdscr.refresh()

    def command_line_display(self):
        x,y = zip(*self.tractor_area.keys())
        xmin, xmax = min(x), max(x)
        ymin, ymax = min(y), max(y)
        for y in range(ymin, ymax + 1):
            string = [f"{y:02d}"]
            for x in range(xmin, xmax + 1):
                if (x,y) not in self.tractor_area.keys():
                    print(f"Possible error at {x,y}")
                block = self.tractor_area[(x,y)]
                string.append('#' if block == 1 else '.')
            print(''.join(string))


def main(intcode: List[int] = None):
    if not intcode:
        intcode = read_input(input_file=_INPUT_FILE)
    drone = Drone(intcode)
    drone.execute_for_grid(82, 82)
    drone.command_line_display()
    return sum(affected for k,affected in drone.tractor_area.items() if k[0] <= 49 and k[1] <= 49)


if __name__ == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        intcode = [int(n) for n in sys.argv[1].split(",")]
    print(f"Afffected points {main(intcode)}")