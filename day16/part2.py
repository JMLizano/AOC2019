import sys
import math
import time
from scipy.sparse import bsr_matrix
from typing import List
from collections import defaultdict


_INPUT_FILE = 'input.txt'
_BASE_PATTERN = [0, 1, 0, -1]


def read_input(input_file: str) -> List[int]:
    with open(file=input_file, mode='r') as f:
        return [int(c) for c in f.readline()]


def simplified_fft(input_list: List[int], iterations: int = 100) -> List[int]:
    """ Simplified function, since offset is so big we only need to sum"""
    for _ in range(iterations):
        for j in reversed(range(len(input_list) - 1)):
            input_list[j] = input_list[j] + input_list[j + 1]
            input_list[j] = int(str(input_list[j])[-1])
    return input_list


if __name__  == '__main__':
    repetition = 10000
    input_numbers = read_input(_INPUT_FILE) * repetition
    if len(sys.argv) > 1:
        input_numbers = [int(c) for c in sys.argv[1]] * repetition
    offset = int(str(''.join(str(i) for i in input_numbers[:7])))
    print(f"Offset {offset}, size: {len(input_numbers)}")
    start = time.time()
    print(''.join(str(c) for c in simplified_fft(input_numbers[offset:], 100)[:8]))
    end_time = time.time()
    print(f"Elapsed time: {end_time-start}")