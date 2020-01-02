import math
from collections import namedtuple, defaultdict
from heapq import heappush, heappop
from typing import Generator, Tuple, List, Set

_INPUT_FILE = 'input.txt'


Point = namedtuple('Point', ['x', 'y'])


def read_input(input_file: str) -> Generator[Point, None, None]:
    with open(file=input_file, mode='r') as f:
        for i, line in enumerate(f.readlines()):
            for j,col in enumerate(list(line)):
                if col == '#':
                    yield Point(j, i)


def distance(a: Point, b: Point) -> float:
    """Compute distance between two points"""
    return math.sqrt(math.pow(b.x - a.x, 2) + math.pow(b.y - a.y, 2))


def angle(a: Point, b: Point) -> int:
    """Compute angle between ortogonal and difference vectors"""
    ang = math.degrees(math.atan2(b.y - a.y, b.x - a.x)) + 90
    return ang + 360 if ang < 0 else ang


def compute_visibility_angles(asteroid: Point, asteroid_list: List[Point]) -> Set[int]:
    return {angle(asteroid, ast) for ast in asteroid_list}


if __name__ == '__main__':
    asteroids = list(read_input(input_file=_INPUT_FILE))
    angles = {ast: compute_visibility_angles(ast, asteroids) for ast in asteroids}
    space_station_location = max(angles.items(), key=lambda x: len(x[1]))
    print(f"Best position for space station location: {space_station_location[0]}")
    print(f"Amount of visible asteroids: {max(len(compute_visibility_angles(ast, asteroids)) for ast in asteroids)}")

