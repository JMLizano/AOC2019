from typing import List


_INPUT_FILE = 'input.txt'


def read_input(input_file: str) -> List[int]:
    with open(file=input_file, mode='r') as f:
        return [int(l) for l in f.readlines()]


def module_required_fuel(module_mass: int) -> int:
    return module_mass // 3 - 2


def total_required_fuel() -> int:
    module_mass_list = read_input(input_file=_INPUT_FILE)
    return sum(module_required_fuel(mm) for mm in module_mass_list)


if __name__  == '__main__':
    print(f"Total required fuel is: {total_required_fuel()}")