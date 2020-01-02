from typing import List
import logging


logging.basicConfig(level=logging.INFO)


_MIN_INPUT = 367479
_MAX_INPUT = 893698


def from_left_great_or_equal(num: List[int]) -> bool:
    return all(num[i + 1] >= num[i] for i in range(len(num) - 1))


def two_numbers_equal(num: List[int]) -> bool:
    return any(num[i] == num[i+1] for i in range(len(num) - 1))


def find_possible_combinations(left: int=_MIN_INPUT, right: int=_MAX_INPUT) -> List[int]:
    possible_numbers = [[int(d) for d in str(num)] for num in range(left, right + 1)]
    logging.info("Analyzing {} numbers".format(len(possible_numbers)))
    return sum(1 for n in possible_numbers if from_left_great_or_equal(n) and two_numbers_equal(n))


if __name__  == '__main__':
    print(f"Number of combinations is: {find_possible_combinations()}")