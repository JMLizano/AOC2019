import logging
logging.basicConfig(level=logging.WARNING)

import sys
sys.path.insert(0, '..')

import copy
import pickle
import os
import tty
tty.setcbreak(sys.stdin)
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
        self.saves = []
        self.current_position = (0, 0)
        self.screen = defaultdict(int)
        self.intcode_computer = IntcodeComputer(intcode, self.get_input, self.generate_output)
        self.offset = 0
        self.score = 1
        self.image = None
    
    def get_input(self):
        os.system('clear')
        print(f"CURENT SCORE: {self.score}")
        self.display_screen()
        c = None
        while c not in ('-1','1', '0'):
            c = sys.stdin.read(1)
            if c == '-':
                c += sys.stdin.read(1)
            if c == '2':
                print(f"Saving game..")
                with open (f'saves/{self.score}.save', 'wb') as f:
                    pickle.dump(self.intcode_computer, f)
            if c == '3':
                c = '-1'
        return int(c)
    
    def generate_output(self, value: int):
        if self.offset == 0:
            self.x = value
            self.offset += 1
        elif self.offset == 1:
            self.y = value
            self.offset += 1
        elif self.offset == 2:
            if self.x == -1 and self.y == 0:
                logging.info(f"Setting score to {value}")
                print(f"Setting score to {value}")
                self.score = value
            else:
                logging.info(f"Setting tile in {self.x},{self.y} with {value}")
                self.screen[(self.x,self.y)] = value
            self.offset = 0  
    
    def load_save(self):
        print(f"Want to load save?")
        go_back = input()
        if go_back != '3':
            print(self.score)
            print("Loading save")
            with open(f"saves/{go_back}.save", 'rb') as f:
                self.intcode_computer = pickle.load(f)

    def execute(self):
        self.load_save()
        while True:
            try:
                self.current_computer = next(self.intcode_computer.process_intcode())
                if self.current_computer is None:
                    print(self.score)
                    return
            except:
                print(self.score)
                self.load_save()

    def command_line_display(self, image):
        for x in range(image.shape[0]):
            string = []
            for y in range(image.shape[1]):
                if image[x,y] == 0:
                    string.append('.')
                if image[x,y] == 1:
                    string.append('|')
                if image[x,y] == 2:
                    string.append('#')
                if image[x,y] == 3:
                    string.append('=')
                if image[x,y] == 4:
                    string.append('*')
            print(''.join(string))

    def display_screen(self):
        if self.image is None:
            self.min_x = min(key[0] for key in self.screen.keys())
            max_x = max(key[0] for key in self.screen.keys())
            min_y = min(key[1] for key in self.screen.keys())
            self.max_y = max(key[1] for key in self.screen.keys())

            size_x = max_x - self.min_x
            size_y = self.max_y - min_y

            self.image = np.zeros(shape=(size_y + 1, size_x + 1))
        for position,color in self.screen.items():
            # Correct coordinates. In the array (0,0) is top left
            self.image[abs(position[1] - self.max_y), abs(position[0] - self.min_x)] = color
        self.command_line_display(self.image)


def main(intcode: List[int] = None):
    if not intcode:
        intcode = read_input(input_file=_INPUT_FILE)
    arc = Arcade(intcode)
    arc.execute()
    print(f"Final score: {arc.score}")


if __name__ == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        intcode = [int(n) for n in sys.argv[1].split(",")]
    main(intcode)