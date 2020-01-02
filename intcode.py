import logging
import sys
from typing import List, Callable, Tuple, Generator
from collections import defaultdict

logging.basicConfig(level=logging.INFO)


_INPUT_FILE = '9-puzzle-input.txt'


def read_input(input_file: str) -> List[int]:
    with open(file=input_file, mode='r') as f:
        return [int(n) for n in f.readline().split(",")]

class IntcodeComputer:

    def __init__(
        self, 
        intcode: List[int], 
        input_hook: Callable[[], int], 
        output_hook: Callable[[int], None], 
        current_pos = 0, 
        relative_base = 0
    ) -> None:
        # Transform list to defaultdict, to provide 'unlimited' memory for the intcode
        intcode_dict = zip(range(len(intcode)), intcode)
        self.intcode = defaultdict(int, intcode_dict)
        self.input_hook = input_hook
        self.output_hook = output_hook
        self.current_pos = 0
        self.relative_base = 0
        self.last_op = None

    def _mode_to_index(self, current_pos, mode:str, delta_pos: int) -> int:
        if mode == '0':
            return self.intcode[current_pos + delta_pos]
        elif mode == '1':
            return current_pos + delta_pos
        elif mode == '2':
            return self.relative_base + self.intcode[current_pos + delta_pos]
        else:
            raise ValueError(f"Unrecognized mode {mode} at position {current_pos}")

    def get_op_parameters(self, current_pos : int, mode: str, num_parameters: int = 2) -> Generator[int, None, None]:
        def get_value(mode: str, delta_pos: int):
            param_index = self._mode_to_index(current_pos, mode, delta_pos)
            return self.intcode[param_index]
        return (get_value(mode[-i], i) for i in range(1, num_parameters + 1))

    def execute_mult_opcode(self, current_pos : int, mode: str) -> List[int]:
        first_value, second_value = self.get_op_parameters(current_pos, mode)
        store_index = self._mode_to_index(current_pos, mode[-3], 3)   
        self.intcode[store_index] = first_value * second_value
        return self.intcode

    def execute_sum_opcode(self, current_pos: int, mode: str) -> List[int]:
        first_value, second_value = self.get_op_parameters(current_pos, mode)
        store_index = self._mode_to_index(current_pos, mode[-3], 3) 
        self.intcode[store_index] = first_value + second_value
        return self.intcode

    def execute_store_opcode(self, current_pos: int, mode: str, condition: Callable) -> List[int]:
        first_value, second_value = self.get_op_parameters(current_pos, mode)
        store_index = self._mode_to_index(current_pos, mode[-3], 3)   
        self.intcode[store_index] = 0 + condition(first_value, second_value)
        return self.intcode

    def execute_jump_opcode(self, current_pos: int, mode: str, condition: Callable) -> Tuple[List[int], int]:
        first_value, second_value = self.get_op_parameters(current_pos, mode)
        delta_pos = 3
        if condition(first_value):
            delta_pos  = second_value - current_pos
        return self.intcode, delta_pos

    def execute_output_opcode(self, current_pos: int, mode: str) -> List[int]:
        value, = self.get_op_parameters(current_pos, mode, num_parameters=1)
        self.output_hook(value)
        return self.intcode

    def execute_input_opcode(self, current_pos: int, mode: str) -> List[int]:
        input_index = self._mode_to_index(current_pos, mode[-1], 1)
        self.intcode[input_index] = self.input_hook()
        return self.intcode

    def execute_adjust_relbase_opcode(self, current_pos: int, mode: str) -> List[int]:
        value, = self.get_op_parameters(current_pos, mode, num_parameters=1)
        logging.info(f"Adding  {value} to relative base")
        self.relative_base += value
        return self.intcode

    def process_intcode_operation(self, current_pos:int) -> List[int]:
        op = str(self.intcode[current_pos])
        if len(op) < 5:
            leading_zeros  = '0' * (5 - len(op))
            op  = f"{leading_zeros}{op}"
        opcode = op[-2:]
        self.last_op = opcode
        mode = op[:-2]
        logging.info(f"Trying to execute operation {opcode} in mode {mode} in pos {current_pos}")
        if opcode == '01':
            return self.execute_sum_opcode(current_pos=current_pos, mode=mode), 4
        elif opcode == '02':
            return self.execute_mult_opcode(current_pos=current_pos, mode=mode), 4
        elif opcode == '03':
            return self.execute_input_opcode(current_pos, mode), 2
        elif opcode == '04':
            return self.execute_output_opcode(current_pos, mode), 2
        elif opcode == '05':
            return self.execute_jump_opcode(current_pos, mode, lambda x: x != 0)
        elif opcode == '06':
            return self.execute_jump_opcode(current_pos, mode, lambda x: x == 0)
        elif opcode == '07':
            return self.execute_store_opcode(current_pos, mode, lambda x,y: x  < y), 4
        elif opcode == '08':
            return self.execute_store_opcode(current_pos, mode, lambda x,y: x == y), 4
        elif opcode == '09':
            return self.execute_adjust_relbase_opcode(current_pos, mode), 2
        elif opcode == '99':
            return self.intcode, len(self.intcode) + 1
        else:
            raise ValueError(f"Unrecognized opcode {opcode} at position {current_pos}")

    def has_next(self) -> bool:
        return self.current_pos < len(self.intcode)

    def process_intcode(self) -> List[int]:
        while(self.current_pos < len(self.intcode)):
            intcode, cursor_increase = self.process_intcode_operation(self.current_pos)
            self.current_pos += cursor_increase
            yield self
        yield None
    
    def execute(self) -> List[int]:
        while(self.current_pos < len(self.intcode)):
            intcode, cursor_increase = self.process_intcode_operation(self.current_pos)
            self.current_pos += cursor_increase
    
    def step(self) -> None:
        while (self.current_pos < len(self.intcode)):
            intcode, cursor_increase = self.process_intcode_operation(self.current_pos)
            self.current_pos += cursor_increase
            if self.last_op == '04': break
        return IntcodeComputer(self.intcode, self.input_hook, self.output_hook, self.current_pos, self.relative_base)