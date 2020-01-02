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
        self.x = 0
        self.y = 0
        self.give_x = True
        self.tractor_area = defaultdict(int)

    def get_input(self):
        # print(f"Giving {self.x, self.y}") 
        if self.give_x:
            self.give_x = False
            return self.x
        else:
            self.give_x = True
            return self.y
    
    def generate_output(self, value: int):
        # print(f"Got {value} on {self.x, self.y}")
        self.tractor_area[(self.x, self.y)] = value
    
    def execute(self):
        self.intcode_computer = IntcodeComputer(self.intcode, self.get_input, self.generate_output)
        while self.intcode_computer.has_next():
            next(self.intcode_computer.process_intcode())
    
    def manual_execute(self):
        user_input = input().split()
        self.x, self.y = int(user_input[0]), int(user_input[1])
        while self.x != 'q':
            self.intcode_computer = IntcodeComputer(self.intcode, self.get_input, self.generate_output)
            while self.intcode_computer.has_next():
                next(self.intcode_computer.process_intcode())
            user_input = input().split()
            self.x, self.y = int(user_input[0]), int(user_input[1])
    
    def find_first_one_in_line(self, line: int):
        start = 1
        found = False
        end = line
        self.y = line   
        while not found:
            self.x = start + (end - start) // 2 + 1
            self.execute()
            if self.tractor_area[(self.x, self.y)] == 1:
                self.x -= 1
                self.execute()
                if self.tractor_area[(self.x, self.y)] == 0:
                    # print(f"Found at {self.x,self.y}")
                    found = True
                end = self.x
            else:
                start = self.x
        return self.x + 1
    
    def check_santa_ship_fit(self, x, y, ship_len):
        self.y = self.y - ship_len + 1
        self.x = x + ship_len - 1
        self.execute()
        return self.tractor_area[(self.x, self.y)] == 1

    def search_first_len(self, ship_len):
        # Try line Y
        # Find first 1 in line Y
        # Check if 100 above is also 1, check if 100 right is also one
        start = ship_len
        end = None
        end_found = False
        found = False
        candidate_x = None
        candidate_y = None
        while not found:
            if not end_found:
                self.y = start * 2
            else:
                self.y = start + (end - start) // 2 + 1
            print(f" **** Trying y={self.y} ****")
            first_x_one = self.find_first_one_in_line(self.y)
            candidate_y = self.y
            candidate_x = first_x_one
            print(f"first 1 in line {self.y}: {first_x_one}")
            if self.check_santa_ship_fit(first_x_one, self.y, ship_len):
                print(f" **** Found candidate at x={first_x_one} y={candidate_y} ****")
                end_found = True
                found = True
                end = candidate_y
                for i in range(1,2):
                    first_x_one = self.find_first_one_in_line(candidate_y - i)
                    if not self.check_santa_ship_fit(first_x_one, candidate_y- 1, ship_len):
                        pass
                    else:
                        print(f"***** Counter at {first_x_one,candidate_y- i} ******")
                        found = False
                if found == True:
                    print(f"***** Found at {candidate_x,candidate_y} ******")

            else:
                start = candidate_y
        return candidate_x, candidate_y - ship_len + 1

        

    def execute_for_grid(self, max_x: int, max_y: int):
        for y in range(max_y):
            self.y = y
            for x in range(max_x):
                self.x = x
                self.execute()

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
    # drone.manual_execute()
    x,y = drone.search_first_len(100)
    # drone.command_line_display()
    return x * 10000 + y


if __name__ == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        intcode = [int(n) for n in sys.argv[1].split(",")]
    print(f"Result: {main(intcode)}")