import logging
import statistics
import time

from collections import namedtuple
from typing import List
from functools import lru_cache

logging.basicConfig(level=logging.INFO)


_INPUT_FILE = 'input.txt'
Spaceobj = namedtuple('spacething', 'orbiting')
space_collection = {}



def time_it(fun, measures = 5):
    times = []
    for _ in range(measures):
        start_time = time.time()
        fun()
        end_time = time.time()
        times.append(end_time-start_time)
    return statistics.mean(times)


def read_input(input_file: str) -> List[str]:
    with open(file=input_file, mode='r') as f:
        return [l.rstrip() for l in f.readlines()]


def get_or_create(space_obj_name: str, orbiting: str = None) -> Spaceobj:
    space_obj = space_collection.get(space_obj_name, None)
    if not space_obj  or (space_obj.orbiting != orbiting and orbiting is not None):
        logging.info("Creating new space object {} orbiting around {}".format(space_obj_name, orbiting))
        space_obj = Spaceobj(orbiting)
        space_collection[space_obj_name] = space_obj
    return space_obj


def process_orbit(orbit_def: str):
    orbit_objects = orbit_def.split(')')
    get_or_create(orbit_objects[0])
    get_or_create(orbit_objects[1], orbit_objects[0])


def get_orbits(space_obj_name: str):
    level = 0 
    orbiting_around = space_collection[space_obj_name].orbiting
    while orbiting_around != None:
        level += 1
        orbiting_around = space_collection[orbiting_around].orbiting
    return level


@lru_cache(maxsize=2000)
def get_orbits_memoize(space_obj_name: str):
    orbiting_around = space_collection[space_obj_name].orbiting
    if orbiting_around is not None:
        return 1 + get_orbits_memoize(orbiting_around)
    return 0

def memoize_sum():
    return sum(get_orbits_memoize(space_obj) for space_obj in space_collection.keys())


def normal_sum():
    return sum(get_orbits(space_obj) for space_obj in space_collection.keys())


def main():
    orbits = read_input(input_file=_INPUT_FILE)
    [process_orbit(orbit) for orbit in orbits]
    logging.info(f"Memoize sum time: {time_it(memoize_sum, measures=10)}")
    logging.info(f"Normal sum time: {time_it(normal_sum, measures=10)}")
    return sum(get_orbits_memoize(space_obj) for space_obj in space_collection.keys())

if __name__  == '__main__':
    logging.info(f"Total number of orbits is {main()}")