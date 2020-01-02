from collections import namedtuple, defaultdict
from itertools import combinations
from typing import List, Tuple
from math import gcd
import time

_INPUT_FILE = 'input.txt'


Vector3 = namedtuple('Vector3', ['x', 'y', 'z'])
Moon = namedtuple('Moon', ['name', 'pos', 'vel'])

pairs = list(combinations([0,1,2,3], 2))

def read_input(input_file: str) -> List[Moon]:
    char_to_remove = {
        ord('<'): None,
        ord('>'): None,
        ord('='): None,
        ord('\n'): None,
        ord('x'): None,
        ord('y'): None,
        ord('z'): None
    }
    with open(file=input_file, mode='r') as f:
        pos = [l.translate(char_to_remove).split(",") for l in f.readlines()]
        return [Moon(i, Vector3(*(int(c) for c in coords)), Vector3(0,0,0)) for i,coords in enumerate(pos)]


def compute_delta_speed(pos: List[int]):
    global pairs
    vel = [0,0,0,0]
    for p1,p2 in pairs:
        if pos[p1] != pos[p2]:
            gravity_factor = pos[p1] > pos[p2]
            vel[p1] += -1 if gravity_factor else 1
            vel[p2] += 1 if gravity_factor else -1
    return vel


def get_cycle(pos, vel):
    initial_state = pos + vel
    i = 0
    while True:
        vel = [x+y for x,y in zip(vel, compute_delta_speed(pos))]
        pos = [x+y for x,y in zip(pos, vel)]
        i += 1
        if pos + vel == initial_state:
            return i


def simulate():
    moons = read_input(_INPUT_FILE)
    cycles = []
    for i in range(3):
        # Get cycle in each dimension: X,Y,Z
        pos = [moon.pos[i] for moon in moons]
        vel = [moon.vel[i] for moon in moons]
        cycle = get_cycle(pos,vel)
        cycles.append(cycle)
    lcm = cycles[0]
    for i in cycles[1:]:
        lcm = lcm*i // gcd(lcm, i)
    print(f"Required steps: {lcm}")


if __name__ == '__main__':
    start_time = time.time()
    simulate()
    end_time = time.time()
    print(f"Time to compute: {end_time-start_time}")
    