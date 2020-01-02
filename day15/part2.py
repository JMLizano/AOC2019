import sys
sys.path.insert(0, '..')

import logging
logging.basicConfig(level=logging.WARNING)

import os
import operator
import numpy as np
import time
from typing import List, Set, Dict, Tuple
from collections import defaultdict, namedtuple
from intcode import IntcodeComputer, read_input
import curses
import copy


Pos = namedtuple('Pos', ['x', 'y'])


_INPUT_FILE='input.txt'


class Drone:
    """ Executes the given intcode program, to play a game"""

    def __init__(self, intcode: List[int]):
        self.intcode = intcode
        self.current_position = (0, 0)
        self.search_space = defaultdict(int)
        self.search_space[self.current_position] = -1
        self.explored = defaultdict(int)
        self.solution_path = []
        self.intcode_computer = IntcodeComputer(intcode, self.get_input, self.generate_output)
        self.moves = {1: (0,1), 2:(0,-1), 3:(1,0), 4:(-1,0)}
        self.oxygen_tank_position = None
        self.oxygen_spread = []
        self._correction_values = None

    def get_input(self):
        return self.input
    
    def generate_output(self, value: int):
        temptative_positon = self.next_position(self.input)
        self.search_space[temptative_positon] = value
        if value != 0:
            self.current_position = temptative_positon
    
    def next_position(self, mov, pos = None) -> Pos:
        if not pos:
            pos = self.current_position
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
            if self.search_space[next_cell] != 0:
                valid_pos.append(next_cell)
        return valid_pos

    def step_back(self):
        # Remove step from solution path
        # print(f"Found dead end, stepping back from {self.current_position}")
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

    def step_forward(self, mov, save=True) -> bool:
        self.input = mov
        self.intcode_computer.step()
        if save:
            self.solution_path.append(mov)

    def explore(self, mov, next_pos):
        self.step_forward(mov, save=False)
        if self.search_space[next_pos] == 0:
            # Hit a wall
            return False
        else:
            self.explored[self.current_position] = 1
            for mov in self.moves.keys():
                next_pos = self.next_position(mov)
                if self.explored[next_pos] == 0:
                    self.explore(mov, next_pos)
            self.step_back()
            return False

    def find_solution(self, mov, next_pos):
        self.step_forward(mov)
        if self.search_space[next_pos] == 2:
            self.step_forward(mov)
            self.oxygen_tank_position = next_pos
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
                    found = self.find_solution(mov, next_pos)
                    if found:
                        return True
            self.step_back()
            return False
    
    @property
    def correction_values(self):
        if not self._correction_values:
            x,y = zip(*self.search_space.keys())
            self._correction_values = (min(x), max(y))
        return self._correction_values
    

    def display(
        self, 
        values: List[Tuple[Tuple[int, int], int]], 
        mapping: Dict[int, int], 
        stdscr = None, pad = None, 
        sleep: float = None,
        line_size: int = 1,
        score_display: str = None,
         
    ) -> None:
        """ Display the values at the given positions by the dictionary"""
        correction_x, correction_y = self.correction_values
        max_y, max_x = stdscr.getmaxyx()
        display_from = 0
        current_line_size = 0
        for x, y, value in ((*position, char) for position, char in values):
            corrected_y = abs(y - correction_y)
            corrected_x = abs(x - correction_x)
            try:
                char, color = mapping[value]
                pad.addch(corrected_y, corrected_x, char, color) 
            except:
                print(corrected_x, corrected_y)
                time.sleep(2)
            if corrected_y > max_y:
                display_from = abs(corrected_y - max_y)
            current_line_size += 1
            if line_size == 1 or current_line_size == line_size:
                pad.refresh(display_from, 0, 0, 0, max_y - 1, max_x - 1)
                current_line_size = 0
                if sleep:
                    time.sleep(sleep)

    def curses_display(self, stdscr):
        stdscr.clear()
        stdscr.refresh()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_CYAN)
        pad = curses.newpad(80,41)
        pad.scrollok(True)
        self.maze_display(stdscr, pad)
        self.display_solution(stdscr, pad)
        self.display_oxygen_spread(stdscr, pad)
        stdscr.getch()

    def maze_display(self, stdscr, pad):
        x,y = zip(*self.search_space.keys())
        xmin, xmax = min(x), max(x)
        ymin, ymax = min(y), max(y)
        mapping = {
            -1: (curses.ACS_CKBOARD, curses.color_pair(1)),
            0: (curses.ACS_CKBOARD, curses.color_pair(0)),
            1: (curses.ACS_BULLET, curses.color_pair(0)),
            2: (curses.ACS_CKBOARD, curses.color_pair(2)),
        }
        cells = (((x,y), self.search_space[(x,y)]) for y in range(ymax, ymin - 1, -1) for x in range(xmin, xmax + 1))
        self.display(cells, mapping, stdscr, pad, 0.05, line_size=41)

    def display_solution(self, stdscr, pad):
        pos_x,pos_y = (0,-1)
        mapping = {0: (curses.ACS_CKBOARD, curses.color_pair(1))}
        score_pad = curses.newpad(1, 25)
        score_pad.refresh
        for step, mov in enumerate(self.solution_path):
            movx, movy = self.moves[mov]
            pos_x += movx
            pos_y += movy
            self.display([((pos_x, pos_y), 0)], mapping, stdscr, pad, 0.05)
            score_pad.addstr(0, 0, f"Number of steps: {step + 1}")
            score_pad.refresh(0, 0, 1, 45, 2, 70)
    
    def display_oxygen_spread(self, stdscr, pad):
        mapping = {2: (curses.ACS_CKBOARD, curses.color_pair(2))}
        minutes_pad = curses.newpad(1, 35)
        for minute, cells in enumerate(self.oxygen_spread):
            self.display(((cell, 2) for cell in cells), mapping, stdscr, pad, 0.02)
            minutes_pad.addstr(0, 0, f"Elapsed minutes: {minute + 1}")
            minutes_pad.refresh(0, 0, 3, 45, 4, 80)
  
    def calculate_oxigen_spread_time(self):
        visited = set(self.oxygen_tank_position)
        to_visit = set(self.valid_positions(self.oxygen_tank_position))
        while to_visit:
            self.oxygen_spread.append(to_visit)
            to_visit_next_min = set()
            for cell in to_visit:
                visited.add(cell)
                to_visit_next_min.update(neighbor for neighbor in self.valid_positions(cell) if neighbor not in visited)
            to_visit = to_visit_next_min
        return len(self.oxygen_spread)

def main(intcode: List[int] = None):
    if not intcode:
        intcode = read_input(input_file=_INPUT_FILE)
    drone = Drone(intcode)
    for i in range(1,5):
        result = drone.find_solution(i, (0,0))
        drone.explore(i, (0,0))
        if result:
            break
    drone.calculate_oxigen_spread_time()
    curses.wrapper(drone.curses_display)

if __name__ == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        intcode = [int(n) for n in sys.argv[1].split(",")]
    main(intcode)