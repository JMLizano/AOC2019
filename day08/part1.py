import logging
import sys
from typing import List, Callable, Generator


logging.basicConfig(level=logging.INFO)


_INPUT_FILE = 'input.txt'
_LAYER_SIZE = 25 * 6


def read_input(input_file: str) -> Generator[int, None, None]:
    with open(file=input_file, mode='r') as f:
        return (int(n) for n in f.readline())


def find_less_zeros_layer(layers: List[List[int]]) -> int:
    def num_zeros(layer: List[int]) -> int:
        return sum(1 for digit in layer if digit == 0)
    return min(layers, key=num_zeros)


def multiply_one_two(layer: List[int]) -> int:
    ones = sum(1 for d in layer if d == 1)  
    twos = sum(1 for d in layer if d == 2)
    return ones * twos


def build_layers(digit_stream: Generator[int, None, None]):
    layers = []
    current_layer = []
    for digit in digit_stream:
        current_layer.append(digit)
        if len(current_layer) >= _LAYER_SIZE:
            layers.append(current_layer)
            current_layer = []
    return layers


def main():
    layers = build_layers(read_input(input_file=_INPUT_FILE))
    less_zero_layer = find_less_zeros_layer(layers)
    return multiply_one_two(less_zero_layer)


if __name__ == '__main__':
    logging.info(f"Number of 1's * 2's in less zero layer: {main()}")