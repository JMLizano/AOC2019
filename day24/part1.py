import sys
from typing import List, Tuple


_NEIGHBORS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def read_input(input_file='input.txt') -> List[int]:
    with open(input_file, 'r') as f:
        return tuple(char  for line in f.readlines() for char in line.strip())


def get_neighbors(position: Tuple[int , int]) -> List[Tuple[int, int]]:
    possible_neighbors = [(position[0] + neighbor[0], position[1] + neighbor[1]) for neighbor in _NEIGHBORS]
    return [neighbor for neighbor in possible_neighbors 
            if neighbor[0] >= 0 and neighbor[0] <= 4 and neighbor[1] >= 0 and neighbor[1] <= 4]


def get_value(position: Tuple[int, int], bug_map: List[str]) -> str:
    return bug_map[position[0] + position[1] * 5]


def get_life_value(position: Tuple[int, int], bug_map: List[str]) -> int:
    return sum(get_value(neighbor, bug_map) == '#' for neighbor in get_neighbors(position))


def get_next_value(position: Tuple[int, int], bug_map: List[str]) -> str:
    life_value = get_life_value(position, bug_map)
    current_value = get_value(position, bug_map)
    if current_value == '.':
        return '#' if life_value == 1 or life_value == 2 else '.'
    else:
        return '#' if life_value == 1 else '.'


def compute_biodiversity_points(bug_map: List[str]) -> int:
    points = 0
    for i in range(1, 26):
        if bug_map[i - 1] == '#':
            print(f"Bug in {i}, adding {2 ** (i-1)}")
            points += 2 ** (i-1)
    return points


def iterate(bug_map: List[str]):
    states = set()
    repeated = False
    while not repeated:
        print(''.join(bug_map))
        bug_map = tuple(get_next_value((x, y), bug_map) for y in range(5) for x in range(5))
        if bug_map in states:
            print("Found repeated state")
            return bug_map
        states.add(bug_map)

def test():
    bug_map = read_input()
    print(''.join(bug_map))
    initial_values = [1, 1, 1, 2, 1, 1, 2, 1, 2, 3, 2, 0, 2, 3, 2, 0, 2, 2, 1, 2, 1, 1, 0, 2, 0]
    for y in range(5):
        for x in range(5):
            print(x,y, get_life_value((x, y), bug_map), get_value((x,y), initial_values))
            assert get_life_value((x, y), bug_map) == get_value((x,y), initial_values)
    bug_map = read_input('test.txt')
    assert compute_biodiversity_points(bug_map) == 2129920

def main():
    bug_map = read_input()
    first_repeated = iterate(bug_map)
    print(''.join(bug_map))
    print(f"Biodiversity points: {compute_biodiversity_points(first_repeated)}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        test()
    else:
        main()
