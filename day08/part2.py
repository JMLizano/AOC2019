
import logging
import sys
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Callable, Generator
from part1 import build_layers, read_input

logging.basicConfig(level=logging.INFO)


_INPUT_FILE = 'input.txt'
_LAYER_SIZE = 25 * 6


def build_image(layers: List[List[int]]) -> List[int]:
    final_image = [0 for _ in range(_LAYER_SIZE)]
    for idx, pixel in enumerate(final_image):
        for layer in layers:
            if layer[idx] != 2:
                final_image[idx] = layer[idx]
                break
    return final_image


def print_image(image_pixels : List[int]) -> None:
    for row in range(6):
        print(image_pixels[(row * 25):(row + 1) * 25])
    image = np.array(image_pixels)
    image = image.reshape(6, 25)
    plt.imshow(image, cmap="gray")
    plt.show()


def main():
    layers = build_layers(read_input(input_file=_INPUT_FILE))
    return build_image(layers)


if __name__ == '__main__':
    print_image(main())