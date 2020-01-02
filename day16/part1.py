import sys
import math
import time
from scipy.sparse import dok_matrix
import numpy as np
from typing import List



_INPUT_FILE = 'input.txt'
_BASE_PATTERN = [0, 1, 0, -1]


def generate_pattern(base_pattern: List[int], size: int) -> List[int]:
    # Repeate each number in base_patter repeat times, and then shift one to left
    matrix_pattern = dok_matrix((size, size))
    for i in range(size):
        for j in range(size):
            for i in range(len(base_pattern)):
                for _ in range(j):
                    matrix_pattern[i,j] = base_pattern[i]
    return matrix_pattern


def zip_with_repeat(long_list, short_list):
    repeat_short = math.ceil(len(long_list) / len(short_list))
    repeated_list = short_list[1:] +  short_list * repeat_short
    return list(zip(long_list, repeated_list))


def read_input(input_file: str) -> List[int]:
    with open(file=input_file, mode='r') as f:
        return [int(c) for c in f.readline()]

def fft(input_list: List[int], base_pattern: List[int], iterations: int = 100) -> List[int]:
    output_list = [0] * len(input_list)
    base_multipliers = [1,-1]
    for _ in range(iterations):
        for j in range(1, len(input_list) + 1):
            sum_result = 0 
            for idx, k in enumerate(range(j-1, len(input_list) + 1, 2 * j)):
                sum_result += sum(a * base_multipliers[ idx % 2 ] for a in input_list[k:k+j])
            output_list[j - 1] = int(str(sum_result)[-1])
        input_list = output_list
    return output_list



if __name__  == '__main__':
    input_numbers = read_input(_INPUT_FILE)
    if len(sys.argv) > 1:
        input_numbers = [int(c) for c in sys.argv[1]]
    start = time.time()
    print(''.join(str(c) for c in fft(input_numbers, _BASE_PATTERN, 100)[:8]))
    end_time = time.time()
    print(f"Elapsed time: {end_time-start}")