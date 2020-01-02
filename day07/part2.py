import sys
sys.path.insert(0, '..')

import copy
import queue
import time
import threading
import logging
from typing import List, Callable
from itertools import permutations
from intcode import  IntcodeComputer

_INPUT_FILE = 'input.txt'
_AMPLIFIER_OUTPUTS = {}


logging.basicConfig(level=logging.INFO)


def read_input(input_file: str) -> List[int]:
    with open(file=input_file, mode='r') as f:
        return [int(n) for n in f.readline().split(",")]


def get_possible_inputs(min_possible_value: int = 5, max_possible_value: int = 9):
    return permutations(range(min_possible_value, max_possible_value + 1))


class Amplifier:
    """ Executes the given intcode program, adjusted by the phase and initial signal value provided

    It will read further required inputs from input_signal, and output any generated signal to 
    output_signal
    """

    def __init__(self, id: int, intcode: List[int], phase: int, initial_signal_value: int = None, input_queue = None, output_queue = None):
        self.intcode = intcode
        self.id = id
        self.phase = phase
        self.input_queue = input_queue
        self.input_queue.put(phase)
        if initial_signal_value != None:
            self.input_queue.put(initial_signal_value)
        self.output_queue = output_queue
        self.intcode_computer = IntcodeComputer(intcode, self.get_input, self.generate_output)
    
    def get_input(self):
        value = self.input_queue.get()
        logging.info(f"Got {value} value from queue in amplifier {self.id}")
        return value
    
    def generate_output(self, x: int):
        self.last_value = x
        self.output_queue.put(x)
    
    def execute(self):
        logging.info(f"Starting amplifier with phase {self.phase}")
        self.intcode_computer.execute()


def main(intcode: List[int] = None):
    if not intcode:
        intcode = read_input(input_file=_INPUT_FILE)
    
    logging.info(f"Executing for intcode {intcode}")
    powers = []
    for inp in get_possible_inputs():
        logging.info(f"Executing for permutation {inp}")
        # For each input we need to execute the code in each amplifier and get the 
        # final output from last amplifier
        queues = [queue.Queue() for i in range(len(inp))]
        amplifiers = []
        for i in range(len(queues)):
            if i == 0:
                amplifiers.append(Amplifier(i, copy.deepcopy(intcode), inp[i], 0, queues[i], queues[(i +1) % 5]))
            else:
                amplifiers.append(Amplifier(i, copy.deepcopy(intcode), inp[i], None, queues[i], queues[(i +1) % 5]))
        workers = [threading.Thread(target=amp.execute) for amp in amplifiers]
        [worker.start() for worker in workers]
        [worker.join() for worker in workers]
        powers.append(amplifiers[4].last_value)
    return max(powers)


if __name__  == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        intcode = [int(n) for n in sys.argv[1].split(",")]

    print(f"Maximum power is {main(intcode)}")