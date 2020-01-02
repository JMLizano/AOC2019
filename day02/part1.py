import sys
from typing import List


_INPUT_FILE = 'input.txt'


def read_input(input_file: str) -> List[int]:
    with open(file=input_file, mode='r') as f:
        return [int(n) for n in f.readline().split(",")]


def execute_mult_opcode(intcode: List[int], current_pos : int) -> List[int]:
    first_value = intcode[intcode[current_pos + 1]]
    second_value = intcode[intcode[current_pos + 2]]
    intcode[intcode[current_pos + 3]] = first_value * second_value
    return intcode


def execute_sum_opcode(intcode: List[int], current_pos: int) -> List[int]:
    first_value = intcode[intcode[current_pos + 1]]
    second_value = intcode[intcode[current_pos + 2]]
    intcode[intcode[current_pos + 3]] = first_value + second_value
    return intcode


def process_intcode_operation(intcode: List[int], current_pos:int) -> List[int]:
    opcode = intcode[current_pos]
    if opcode == 1:
        return execute_sum_opcode(intcode=intcode, current_pos=current_pos), opcode
    elif opcode == 2:
        return execute_mult_opcode(intcode=intcode, current_pos=current_pos), opcode
    elif opcode == 99:
        return intcode, opcode
    else:
        raise ValueError(f"Unrecognized opcode {opcode} at position {current_pos}")


def process_intcode(intcode: List[int]) -> List[int]:
    current_pos = 0
    opcode = None
    while(current_pos < len(intcode) and opcode != 99):
        intcode, opcode = process_intcode_operation(intcode, current_pos)
        current_pos += 4
    return intcode


def main(intcode: List[int] = None, value1: int = 12, value2: int = 2):
    if not intcode:
        intcode = read_input(input_file=_INPUT_FILE)
        intcode[1] = value1
        intcode[2] = value2
    return process_intcode(intcode)


if __name__  == '__main__':
    intcode = None
    value1 = 12
    value2 = 2
    if len(sys.argv) > 1 and len(sys.argv) < 3:
        intcode = [int(n) for n in sys.argv[1].split(",")]
    elif len(sys.argv) > 2:
        value1 = int(sys.argv[1])
        value2 = int(sys.argv[2])
    result = main(intcode, value1, value2)
    print(f"Value at position 0 after processing: {result[0]}")