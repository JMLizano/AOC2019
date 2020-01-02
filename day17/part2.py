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
        self.input = 1
        self.routine_index = 0
        self.main_rutine = [ord('A'), 44, ord('A'), 44, ord('B'), 44, ord('C'), 44, ord('B'), 44, ord('C'), 44, ord('B'), 44, ord('C'), 44, ord('B'), 44, ord('A'), 10]
        self.A = [ord('R'), 44, ord('6'), 44, ord('L'), 44, ord('1'), ord('2'), 44, ord('R'), 44, ord('6'), 10] 
        self.B = [ord('L'), 44, ord('1'), ord('2'), 44, ord('R'), 44, ord('6'), 44, ord('L'), 44, ord('8'), 44, ord('L'), 44, ord('1'), ord('2'), 10] 
        self.C = [ord('R'), 44, ord('1'), ord('2'), 44, ord('L'), 44, ord('1'), ord('0'), 44, ord('L'), 44, ord('1'), ord('0'), 10]
        self.video_feed = [110, 10]
        self.routines = self.A + self.B + self.C
        self.colllected_dust = []

    def get_input(self):
        if self.input == 1:
            value = self.main_rutine[self.routine_index]
            self.routine_index += 1
            if self.routine_index == len(self.main_rutine):
                self.routine_index = 0
                self.input = 2
            return value
        elif self.input == 2:
            value = self.routines[self.routine_index]
            self.routine_index += 1
            if self.routine_index == len(self.routines):
                self.routine_index = 0
                self.input = 3
            return value
        elif self.input == 3:
            value = self.video_feed[self.routine_index]
            self.routine_index += 1
            return value
        return 0
    
    def generate_output(self, value: int):
        self.colllected_dust.append(value)

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

    def next_robot_position(self, robot_pos, robot_orientation) -> Pos:
        if robot_orientation == 2:
            return (robot_pos[0], robot_pos[1] - 1)
        elif robot_orientation == 3:
            return (robot_pos[0] -1, robot_pos[1])
        elif robot_orientation == 4:
            return (robot_pos[0] + 1, robot_pos[1])
        elif robot_orientation == 5:
            return (robot_pos[0], robot_pos[1] + 1)

    def get_next_orientation(self, orientation, turn):
        if turn == 'L':
            if orientation == 2: return 3
            elif orientation == 3: return 5
            elif orientation == 4: return 2
            elif orientation == 5: return 4
        elif turn == 'R':
            if orientation == 2: return 4
            elif orientation == 3: return 2
            elif orientation == 4: return 5
            elif orientation == 5: return 3

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

    def greedy_solver(self):
        robot_pos = self.robot_pos
        robot_orientation = 2
        total_scaffold = sum(v for v in self.search_space.values() if v == 1)
        print(f"Total scaffold to cover {total_scaffold}")
        covered = 0
        movements = []
        while covered < total_scaffold:
            avance = 0
            next_robot_pos = self.next_robot_position(robot_pos, robot_orientation)
            while self.search_space[next_robot_pos] == 1:
                avance += 1
                robot_pos = next_robot_pos
                next_robot_pos = self.next_robot_position(robot_pos, robot_orientation)
            print(f"Advanced {avance}, covered {covered}")
            avance += 1
            movements.append(avance)
            covered += avance
            avance = 0
            next_robot_orientation = self.get_next_orientation(robot_orientation, 'L')
            next_robot_pos = self.next_robot_position(robot_pos, next_robot_orientation)
            if self.search_space[next_robot_pos] == 1:
                robot_pos = next_robot_pos
                robot_orientation = next_robot_orientation
                movements.append('L')
                print(f"Turning left")
            else:
                next_robot_orientation = self.get_next_orientation(robot_orientation, 'R')
                next_robot_pos = self.next_robot_position(robot_pos, next_robot_orientation)
                if self.search_space[next_robot_pos] == 1:
                    robot_pos = next_robot_pos
                    robot_orientation = next_robot_orientation
                    movements.append('R')
                    print(f"Turning right")
                else:
                    raise("Dead end")
        return movements

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
    return robot.colllected_dust


if __name__ == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        intcode = [int(n) for n in sys.argv[1].split(",")]
    result = main(intcode)
    print(f"Collected dust: {result[-1]}")