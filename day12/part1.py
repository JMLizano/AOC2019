from collections import namedtuple, defaultdict
from itertools import combinations
from typing import List, Tuple


_INPUT_FILE = 'input.txt'


Vector3 = namedtuple('Vector3', ['x', 'y', 'z'])
Moon = namedtuple('Moon', ['name', 'pos', 'vel'])


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


def compute_delta_speed(moon1: Moon, moon2: Moon) -> Tuple[List[int], List[int]]:
    moon1_speed = [0 for _ in range(len(moon1.pos))]
    moon2_speed = [0 for _ in range(len(moon1.pos))]
    for coord in range(len(moon1.pos)):
        if moon1.pos[coord] != moon2.pos[coord]:
            gravity_factor = moon1.pos[coord] > moon2.pos[coord]
            moon1_speed[coord] = -1 if gravity_factor else 1
            moon2_speed[coord] = 1 if gravity_factor else -1
    return moon1_speed, moon2_speed


def update_velocity(moons: List[Moon]):
    def initial_delta_speed(): return [0,0,0]
    
    delta_speed = defaultdict(initial_delta_speed)

    for moon1, moon2 in combinations(moons, 2):
        delta1, delta2 = compute_delta_speed(moon1, moon2)
        delta_speed[moon1] = [x+y for x,y in zip(delta_speed[moon1], delta1)]
        delta_speed[moon2] = [x+y for x,y in zip(delta_speed[moon2], delta2)]
   
    new_moons = []
    for moon in moons:
       vel = Vector3(*(x+y for x,y in zip(delta_speed[moon], moon.vel)))
       pos = Vector3(*(x+y for x,y in zip(moon.pos, vel)))
       new_moons.append(Moon(moon.name, pos, vel))
    return new_moons


def compute_kinetic_energy(moons: List[Moon]) -> int:
    return sum(sum(abs(x) for x in moon.pos) * sum(abs(x) for x in moon.vel) for moon in moons)


def position_identifier(moons: List[Moon]) -> str:
    pos_str = ''.join(''.join(str(x) for x in moon.pos) for moon in moons)
    vel_str = ''.join(''.join(str(x) for x in moon.vel) for moon in moons)
    return pos_str + vel_str


def simulate():
    positions = set()
    moons = read_input(_INPUT_FILE)
    i = 0
    for i in range(1000):
        print(f"**** ITERATION: {i} ****")
        [print(moon) for moon in moons]
        moons = update_velocity(moons)
        pos_id = position_identifier(moons)
        if pos_id in positions:
            print(f"Repeated at step {i + 1}")
            break
        positions.add(pos_id)
        i += 1
    print(f"Total energy: {compute_kinetic_energy(moons)}")


if __name__ == '__main__':
    simulate()