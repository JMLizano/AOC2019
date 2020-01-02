import sys
from typing import List, Tuple
from functools import lru_cache

_NEIGHBORS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def read_input(input_file='input.txt') -> List[int]:
    with open(input_file, 'r') as f:
        return tuple(char  for line in f.readlines() for char in line.strip())


def get_neighbors(position: Tuple[int , int], current_level: str,  upper_level: str, lower_level: str) -> List[str]:
    possible_neighbors = [(position[0] + neighbor[0], position[1] + neighbor[1]) for neighbor in _NEIGHBORS]
    neighbor_values = []
    for neighbor in possible_neighbors:
        if neighbor[0] >= 0 and neighbor[0] <= 4 and neighbor[1] >= 0 and neighbor[1] <= 4:
            if neighbor in [(2,2)]:
                if lower_level:
                    if position == (1,2):
                        neighbor_values += [get_value((0, y), lower_level) for y in range(5)]
                    elif position == (2,1):
                        neighbor_values += [get_value((x, 0), lower_level) for x in range(5)]
                    elif position == (3,2):
                        neighbor_values += [get_value((4, y), lower_level) for y in range(5)]
                    elif position == (2,3):
                        neighbor_values += [get_value((x, 4), lower_level) for x in range(5)]
            else:
                neighbor_values.append(get_value(neighbor, current_level))
        else:
            if upper_level:
                upper_level_position = None
                if neighbor[0] < 0:
                    upper_level_position = (1,2)
                if neighbor[0] > 4:
                    upper_level_position = (3,2)
                if neighbor[1] < 0:
                    upper_level_position = (2,1)
                if neighbor[1] > 4:
                    upper_level_position = (2,3)
                neighbor_values.append(get_value(upper_level_position, upper_level))
    return neighbor_values


def get_value(position: Tuple[int, int], bug_map: List[str]) -> str:
    return bug_map[position[0] + position[1] * 5]


def get_life_value(position: Tuple[int, int], bug_map: str,  upper_level: str, lower_level: str) -> int:
    return sum(neighbor_value == '#' for neighbor_value in get_neighbors(position, bug_map, upper_level, lower_level))


def get_next_value(position: Tuple[int, int], bug_map: str, upper_level: str, lower_level: str) -> str:
    if position == (2,2):
        return '?'
    life_value = get_life_value(position, bug_map,upper_level, lower_level)
    current_value = get_value(position, bug_map)
    if current_value == '.':
        return '#' if life_value == 1 or life_value == 2 else '.'
    else:
        return '#' if life_value == 1 else '.'


def sum_bugs(bug_map: str) -> int:
    return sum(char == '#' for char in bug_map)


@lru_cache(maxsize=400)
def get_hash(level: str) -> int:
    return hash(level)


@lru_cache(maxsize=400)
def get_next_state(current: str, upper:str, lower: str) -> str:
    if get_hash(current) == get_hash(upper) == get_hash(lower) == 6129554674101551624:
        # All three levels don't have bugs
        return current
    else:
        return ''.join(get_next_value((x, y), current, upper, lower) for y in range(5) for x in range(5))


def iterate(bug_map: str):
    levels = ['.........................'] * 401
    levels[200] = bug_map
    for _ in range(200):
        new_levels = []
        for idx, level in enumerate(levels):
            if idx > 0 and idx < 400:
                new_levels.append(get_next_state(current=level, upper=levels[idx - 1], lower=levels[idx + 1]))
            elif idx == 0:
                new_levels.append(get_next_state(current=level, upper=None, lower=levels[idx + 1]))
            elif idx == 400:
                new_levels.append(get_next_state(current=level, upper=levels[idx - 1], lower=None))
        levels = new_levels
    return sum(sum_bugs(level) for level in levels)


def print_bug_map(bug_map: str):
    for y in range(5):
        print(bug_map[y*5:y*5 + 5])

def test():
    bug_map = read_input('test2.txt')
    levels = ['.........................'] * 11
    levels[5] = bug_map
    for minute in range(10):
        new_levels = []
        for idx, level in enumerate(levels):
            if idx > 0 and idx < 10:
                new_levels.append(get_next_state(current=level, upper=levels[idx - 1], lower=levels[idx + 1]))
            elif idx == 0:
                new_levels.append(get_next_state(current=level, upper=None, lower=levels[idx + 1]))
            elif idx == 10:
                new_levels.append(get_next_state(current=level, upper=levels[idx - 1], lower=None))
        levels = new_levels
        print(f"**** Minute: {minute} ****")
        for idx,level in enumerate(levels):
            print(f"\nDepth: {idx - 5}")
            print_bug_map(level)
        print(f"Total number of bugs: {sum(sum_bugs(level) for level in levels)}")

def main():
    bug_map = read_input()
    number_bugs = iterate(bug_map)
    print(f"Total number of bugs: {number_bugs}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        test()
    else:
        main()
