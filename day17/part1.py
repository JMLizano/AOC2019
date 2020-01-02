import sys
sys.path.insert(0, '..')

import logging
logging.basicConfig(level=logging.WARNING)

import os
import numpy as np
import time
from typing import List, Set
from collections import defaultdict, namedtuple
from intcode import IntcodeComputer, read_input
import curses
import copy

Pos = namedtuple('Pos', ['x', 'y'])

logging.basicConfig(level=logging.INFO)

_INPUT_FILE='input.txt'


class VacuumRobot:
    """ Executes the given intcode program, to play a game"""

    def __init__(self, intcode: List[int]):
        self.intcode = intcode
        self.x = 0
        self.y = 0
        self.current_position = (self.x, self.y)
        self.search_space = defaultdict(int)
        self.intcode_computer = IntcodeComputer(intcode, self.get_input, self.generate_output)
        self.moves = {1: (0,1), 2:(0,-1), 4:(1,0), 3:(-1,0)}
        self.alignment_points = []

    def get_input(self):
        return 0
    
    def generate_output(self, value: int):
        print(f"Got {value} on {self.current_position}")
        if value == 35:
            # scaffold
            self.search_space[self.current_position] = 1
            self.x += 1
        elif value == 46:
            # open space
            self.search_space[self.current_position] = 0
            self.x += 1
        elif value == 10:
            # new line
            self.x = 0
            self.y += 1
        elif value == 94:
            # Robot up
            self.search_space[self.current_position] = 2
            self.x += 1
        elif value == 60:
            # Robot izq
            self.search_space[self.current_position] = 3
            self.x += 1
        elif value == 62:
            # Robot der
            self.search_space[self.current_position] = 4
            self.x += 1
        elif value == 118:
            # Robot down
            self.search_space[self.current_position] = 5
            self.x += 1
        self.current_position = (self.x, self.y)
    
    def get_alignments(self):
        for position, value in self.search_space.items():
            if value == 1 and len(self.valid_positions(position)) >= 3:
                logging.warning(f"Found alignment point at {position}")
                self.alignment_points.append(position)
    
    def get_alignments_value(self):
        return sum(x * y for x,y in self.alignment_points)

    def execute(self):
        while self.intcode_computer.has_next():
            next(self.intcode_computer.process_intcode())
    
    def next_position(self, mov, pos = None) -> Pos:
        if mov == 1:
            return (pos[0], pos[1] +1)
        elif mov == 2:
            return (pos[0], pos[1] -1)
        elif mov == 3:
            return (pos[0] + 1, pos[1])
        elif mov == 4:
            return (pos[0] - 1, pos[1])

    def valid_positions(self, pos):
        valid_pos = []
        for mov in self.moves.keys():
            next_cell = self.next_position(mov, pos)
            if next_cell in self.search_space.keys() and self.search_space[next_cell] == 1:
                valid_pos.append(next_cell)
        return valid_pos
    
    def curses_display(self, stdscr):
        stdscr.clear()
        stdscr.refresh()
        x,y = zip(*self.search_space.keys())
        xmin, xmax = min(x), max(x)
        ymin, ymax = min(y), max(y)
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                block = self.search_space[(x,y)]
                character = "#" if block == 0 else "."
                stdscr.addstr(abs(x - xmin),abs(y - ymin), character) 
                stdscr.refresh()

    def command_line_display(self):
        x,y = zip(*self.search_space.keys())
        xmin, xmax = min(x), max(x)
        ymin, ymax = min(y), max(y)
        for y in range(ymin, ymax + 1):
            string = [f"{y:02d}"]
            for x in range(xmin, xmax + 1):
                if (x,y) not in self.search_space.keys():
                    print(f"Possible error at {x,y}")
                block = self.search_space[(x,y)]
                if (x,y) in self.alignment_points:
                    string.append('O')
                elif block == 2:
                    string.append('>')
                else: 
                    string.append("#" if block == 1 else ".")
            print(''.join(string))


def main(intcode: List[int] = None):
    if not intcode:
        intcode = read_input(input_file=_INPUT_FILE)
    robot = VacuumRobot(intcode)
    robot.execute()
    # curses.wrapper(robot.curses_display)
    robot.get_alignments()
    robot.command_line_display()
    return robot.get_alignments_value()


if __name__ == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        intcode = [int(n) for n in sys.argv[1].split(",")]
    print(f"Alignment value; {main(intcode)}")