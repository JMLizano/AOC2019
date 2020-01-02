import sys
import logging
from part1 import _INPUT_FILE, read_input
from typing import Generator, Tuple, List


logging.basicConfig(level=logging.INFO)


def str_to_location(current_loc: Tuple[int, int], mov: str, current_steps: int) -> Tuple[int, int]:
    direction = mov[0]
    length = int(mov[1:]) 
    if direction == 'U':
        return (current_loc[0], current_loc[1] + length), {(current_loc[0], current_loc[1] + l): current_steps+l for l in range(length + 1)}, current_steps + length
    elif direction == 'D':
        return (current_loc[0], current_loc[1] - length), {(current_loc[0], current_loc[1] - l): current_steps+l for l in range(length + 1)}, current_steps + length
    elif direction == 'R':
        return (current_loc[0] + length, current_loc[1]), {(current_loc[0] + l, current_loc[1]): current_steps+l for l in range(length + 1)}, current_steps + length
    elif direction == 'L':
        return (current_loc[0] - length, current_loc[1]), {(current_loc[0] - l, current_loc[1]): current_steps+l for l in range(length + 1)}, current_steps + length 


def find_intersections(cable_paths: Generator[Tuple[str, str], None, None]):
    current_loc_a = (0,0)
    current_loc_b = (0,0)
    current_steps_a = 0
    current_steps_b = 0
    cable_a_locations = {(0,0): 0}
    cable_b_locations = {(0,0): 0}
    for mov_a, mov_b in cable_paths:
        current_loc_a, positions_a, current_steps_a = str_to_location(current_loc_a, mov_a, current_steps_a)
        cable_a_locations = {**positions_a, **cable_a_locations}
        current_loc_b, positions_b, current_steps_b = str_to_location(current_loc_b, mov_b, current_steps_b)
        cable_b_locations = {**positions_b, **cable_b_locations}
    intersection = set(cable_a_locations.keys()).intersection(set(cable_b_locations.keys()))
    return [cable_a_locations[intpoint] + cable_b_locations[intpoint] for intpoint in intersection if intpoint != (0,0)]


def main(cable_paths: Generator[Tuple[str, str], None, None]):
    intersection_points = find_intersections(cable_paths)
    return min(intersection_points)

if __name__  == '__main__':
    if len(sys.argv) > 2:
        cable_path_a = sys.argv[1].split(',')
        cable_path_b = sys.argv[2].split(',')
        cable_paths = zip(cable_path_a, cable_path_b)
    else:
        cable_paths = read_input(input_file=_INPUT_FILE)
    print(f"Minimum number of steps is: {main(cable_paths)}")