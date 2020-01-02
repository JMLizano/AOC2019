import sys
sys.path.insert(0, '..')
import logging
from typing import List, Callable
from intcode import  IntcodeComputer, read_input


_INPUT_FILE = 'input.txt'
_AMPLIFIER_OUTPUTS = {}


logging.basicConfig(level=logging.INFO)


def main(intcode: List[int] = None):
    if not intcode:
        intcode = read_input(input_file=_INPUT_FILE)
    intcode_computer = IntcodeComputer(intcode, lambda : 2, lambda x: print(f"BOOST keycode: {x}"))
    intcode_computer.execute()
    

if __name__  == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        intcode = [int(n) for n in sys.argv[1].split(",")]
    main(intcode)