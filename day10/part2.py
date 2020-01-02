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


def group_asteroids_by_angle(space_station, asteroid_list):
    angle_dict = defaultdict(list)
    for ast in asteroids:
        # Each dict entry holds a heap ordered by distance to asteroid
        heappush(angle_dict[angle(space_station, ast)], (distance(space_station, ast), ast))
    return angle_dict


def eliminate_asteroids(angle_dict):
    eliminated = 0
    last_eliminated = None
    while True:
        for ang in sorted(angle_dict.keys()):
            if angle_dict[ang]:
                last_eliminated = heappop(angle_dict[ang])
                eliminated += 1
                print(f"Vaporizing asteroid #{eliminated} at {last_eliminated}")
                if eliminated == 200:
                    return last_eliminated[1]


if __name__ == '__main__':
    asteroids = list(read_input(input_file=_INPUT_FILE))
    angle_dict = group_asteroids_by_angle(Point(13, 17), asteroids)
    asteroid_200_pos = eliminate_asteroids(angle_dict)
    print(f"Answer: {asteroid_200_pos[0] * 100 + asteroid_200_pos[1]}")

