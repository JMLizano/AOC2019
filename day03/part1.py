import sys
import logging
from typing import Generator, Tuple, List
from functools import partial


logging.basicConfig(level=logging.INFO)


_INPUT_FILE = 'input.txt'


def read_input(input_file: str) -> Generator[Tuple[str, str], None, None]:
    with open(file=input_file, mode='r') as f:
        lines  = f.readlines()
        return zip(lines[0].split(","), lines[1].split(","))


def str_to_location(current_loc: Tuple[int, int], mov: str) -> Tuple[int, int]:
    direction = mov[0]
    length = int(mov[1:]) 
    if direction == 'U':
        return (current_loc[0], current_loc[1] + length), set((current_loc[0], current_loc[1] + l) for l in range(length + 1))
    elif direction == 'D':
        return (current_loc[0], current_loc[1] - length), set((current_loc[0], current_loc[1] - l) for l in range(length + 1))
    elif direction == 'R':
        return (current_loc[0] + length, current_loc[1]), set((current_loc[0] + l, current_loc[1]) for l in range(length + 1)) 
    elif direction == 'L':
        return (current_loc[0] - length, current_loc[1]), set((current_loc[0] - l, current_loc[1]) for l in range(length + 1)) 


def find_intersections(cable_paths: Generator[Tuple[str, str], None, None]):
    current_loc_a = (0,0)
    current_loc_b = (0,0)
    cable_a_locations = set()
    cable_b_locations = set()
    for mov_a, mov_b in cable_paths:
        current_loc_a, positions_a = str_to_location(current_loc_a, mov_a)
        cable_a_locations = cable_a_locations.union(positions_a)
        current_loc_b, positions_b = str_to_location(current_loc_b, mov_b)
        cable_b_locations = cable_b_locations.union(positions_b)
        logging.info("Cable positions (a,b) {} {}".format(current_loc_a, current_loc_b))
    return list(intpoint for intpoint in cable_a_locations.intersection(cable_b_locations)  if intpoint != (0,0))


def manhattan_distance(point_a: Tuple[int, int], point_b: Tuple[int, int]):
    return sum(abs(p - q) for p,q in zip(point_a, point_b))


def find_closest_intersection_distance(intersection_points: List[Tuple[int, int]]):
    return min(manhattan_distance(p, (0,0)) for p in intersection_points)


def main(cable_paths: Generator[Tuple[str, str], None, None]):
    intersection_points = find_intersections(cable_paths)
    return find_closest_intersection_distance(intersection_points)


if __name__  == '__main__':
    if len(sys.argv) > 2:
        cable_path_a = sys.argv[1].split(',')
        cable_path_b = sys.argv[2].split(',')
        cable_paths = zip(cable_path_a, cable_path_b)
    else:
        cable_paths = read_input(input_file=_INPUT_FILE)
    print(f"Closest intersection distance is: {main(cable_paths)}")