import sys
import copy
import logging
from typing import List, Callable, Tuple
from itertools import permutations


_INPUT_FILE = 'input.txt'
_AMPLIFIER_OUTPUTS = {}


logging.basicConfig(level=logging.INFO)


def read_input(input_file: str) -> List[int]:
    with open(file=input_file, mode='r') as f:
        return [int(n) for n in f.readline().split(",")]


def get_possible_inputs(max_possible_value: int = 4):
    return permutations(range(max_possible_value + 1))


def get_parameters(intcode: List[int], current_pos : int, mode: str) -> List[int]:
    def get_by_mode(mode: str, delta_pos: int):
        if mode == '0':
            return intcode[intcode[current_pos + delta_pos]]
        elif mode == '1':
            return intcode[current_pos + delta_pos]
        else:
            raise ValueError(f"Unrecognized mode {mode} at position {current_pos}")
    mode_first_value = mode[-1]
    mode_second_value = mode[-2]
    return get_by_mode(mode_first_value, 1), get_by_mode(mode_second_value, 2)


def execute_mult_opcode(intcode: List[int], current_pos : int, mode: str) -> List[int]:
    first_value, second_value = get_parameters(intcode, current_pos, mode)
    intcode[intcode[current_pos + 3]] = first_value * second_value
    return intcode


def execute_sum_opcode(intcode: List[int], current_pos: int, mode: str) -> List[int]:
    first_value, second_value = get_parameters(intcode, current_pos, mode)
    intcode[intcode[current_pos + 3]] = first_value + second_value
    return intcode


def execute_store_opcode(intcode: List[int], current_pos: int, mode: str, condition: Callable) -> List[int]:
    first_value, second_value = get_parameters(intcode, current_pos, mode)    
    intcode[intcode[current_pos + 3]] = 0 + condition(first_value, second_value)
    return intcode


def execute_jump_opcode(intcode: List[int], current_pos: int, mode: str, condition: Callable) -> Tuple[List[int], int]:
    first_value, second_value = get_parameters(intcode, current_pos, mode)
    delta_pos = 3
    if condition(first_value):
        delta_pos  = second_value - current_pos
    return intcode, delta_pos


def process_intcode_operation(intcode: List[int], current_pos:int, input_f: Callable, output_f: Callable) -> List[int]:
    op = str(intcode[current_pos])
    if len(op) < 5:
        leading_zeros  = '0' * (5 - len(op))
        op  = f"{leading_zeros}{op}"
    opcode = op[-2:]
    mode = op[:-2]
    logging.info(f"Trying to execute operation {opcode} in mode {mode} in pos {current_pos}")
    if opcode == '01':
        return execute_sum_opcode(intcode=intcode, current_pos=current_pos, mode=mode), 4
    elif opcode == '02':
        return execute_mult_opcode(intcode=intcode, current_pos=current_pos, mode=mode), 4
    elif opcode == '03':
        intcode[intcode[current_pos + 1]] = int(input_f())
        return intcode, 2
    elif opcode == '04':
        value = None
        if mode[-1] == '0':
            value = intcode[intcode[current_pos + 1]]
        elif mode[-1] == '1':
            value = intcode[current_pos + 1]
        output_f(value)
        return intcode, 2
    elif opcode == '05':
        return execute_jump_opcode(intcode, current_pos, mode, lambda x: x != 0)
    elif opcode == '06':
        return execute_jump_opcode(intcode, current_pos, mode, lambda x: x == 0)
    elif opcode == '07':
        return execute_store_opcode(intcode, current_pos, mode, lambda x,y: x  < y), 4
    elif opcode == '08':
        return execute_store_opcode(intcode, current_pos, mode, lambda x,y: x == y), 4
    elif opcode == '99':
        return intcode, len(intcode) + 1
    else:
        raise ValueError(f"Unrecognized opcode {opcode} at position {current_pos}")


def process_intcode(intcode: List[int], input_f: Callable, output_f: Callable) -> List[int]:
    current_pos = 0
    while(current_pos < len(intcode)):
        intcode, cursor_increase = process_intcode_operation(intcode, current_pos, input_f, output_f)
        current_pos += cursor_increase
    return intcode


def main(intcode: List[int] = None):
    if not intcode:
        intcode = read_input(input_file=_INPUT_FILE)
    
    logging.info(f"Executing for intcode {intcode}")
    powers = []
    for inp in get_possible_inputs():
        # For each input we need to execute the code in each amplifier and get the 
        # final output from last amplifier
        ampl_input = [0]
        for value in inp:
            values = [ampl_input.pop(), value]
            print(f"DEFINED VALUES {values}")

            def input_var():
                print(f"EXTRACTING FROM {values}")
                return values.pop()
            
            def output_ampl(x):
                print(f"APPENDING {x} to {ampl_input}")
                ampl_input.append(x)
            process_intcode(copy.deepcopy(intcode), input_var, output_ampl)
        powers.append(ampl_input)
    return max(powers)

if __name__  == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        print(sys.argv)
        intcode = [int(n) for n in sys.argv[1].split(",")]
    print(f"Maximum power is {main(intcode)}")