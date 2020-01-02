# How many steps is the shortest path that collects all of the keys?

# Ideas:
# - Try A* with number of remaining keys as heuristic
# - This is not an exploring algorithm, you have the whole map. And where
# the keys and doors are
import math
import string
from collections import defaultdict
from heapq import heappop, heappush
from typing import Dict, List, Set, Tuple, Callable

len_shortest_path_pairs = {} # dictionary to hold min steps between all pairs of keys
doors_key_collected: Set[str] # List of Doors for which we have the key
movement_set = {
    'up': (0 , -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0)
}

def read_map(input_file: str) -> Tuple[Dict[Tuple[int, int], str], Tuple[int, int], Dict[str, Tuple[int, int]]]:
    map_dict = {}
    key_positions = {}
    initial_pos = []
    with open(input_file, 'r') as f:
        for y, line in enumerate(f.readlines()):
            for x, char in enumerate(line.strip()):
                map_dict[x,y] = char
                if char in string.ascii_lowercase:
                    key_positions[char] = (x,y)
                elif char == '@':
                    initial_pos.append((x,y))
    return map_dict, initial_pos, key_positions

def search_heuristic(position:  Tuple[int, int], target: Tuple[int, int]) -> int:
    return math.sqrt((target[0] - position[0]) ** 2 + (target[1] - position[1]) ** 2)


def neighbors(search_space: Dict[Tuple[int, int], str], position: Tuple[int, int]) -> List[Tuple[int, int]]:
    neighbors_list = []
    for mov in movement_set.values():
        tempative_neighbor = (position[0] + mov[0], position[1] + mov[1])
        if (tempative_neighbor in search_space.keys() and 
           search_space[tempative_neighbor] != '#'):
           neighbors_list.append(tempative_neighbor)
    return neighbors_list


def build_path_backwards(
    target: Tuple[int,int], 
    came_from: Dict[Tuple[int, int], List[int]]
) -> List[Tuple[int, int]]:
    target_path = []
    current = target
    while came_from[current]:
        target_path.append(current)
        current = came_from[current]
    return list(reversed(target_path))


def a_star_search(
    search_space: Dict[Tuple[int, int], str],
    initial_position: Tuple[int, int], 
    target: Tuple[int, int], 
    heuristic: Callable
) -> List[Tuple[int, int]]:

    came_from: Dict[Tuple[int, int], List[int]] = defaultdict(list)
    
    # G(n) : Cost of shortest path to n 
    g_score: Dict[Tuple[int, int], int] = defaultdict(lambda: math.inf)
    g_score[initial_position] = 0

    # F(n): G(n) + h(n), where h is the heuristic function
    f_score: Dict[Tuple[int, int], int] = defaultdict(lambda: math.inf)
    f_score[initial_position] = heuristic(initial_position, target)

    # Initial set of visited nodes
    open_set : List = []
    heappush(open_set, (f_score[initial_position], initial_position))
    while open_set:
        current = heappop(open_set)
        if current[1] == target:
            return build_path_backwards(current[1], came_from)
        
        for neighbor in neighbors(search_space, current[1]):
            if g_score[current[1]] + 1 < g_score[neighbor]:
                came_from[neighbor] = current[1]
                g_score[neighbor] = g_score[current[1]] + 1
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, target)
                if neighbor not in open_set:
                    heappush(open_set, (f_score[neighbor], neighbor))
    return []


def shortest_path(
    search_space: Dict[Tuple[int, int], str], 
    position: Tuple[int,int], 
    target: Tuple[int,int]
) -> List[int]:
    """ Find the shortest path between position and given key
    
    TODO: It should collect keys on the go."""
    return a_star_search(search_space, position, target, search_heuristic)


def len_shortest_path(
    search_space: Dict[Tuple[int, int], str], 
    position: Tuple[int,int], 
    target: Tuple[int,int]
) -> int:
    if (position, target) in len_shortest_path_pairs.keys():
        return len_shortest_path_pairs[(position, target)]
    elif (target, position) in len_shortest_path_pairs.keys():
       return len_shortest_path_pairs[(target, position)]
    len_shortest_path_pairs[(target, position)] = len(shortest_path(search_space, position, target))
    return len_shortest_path_pairs[(target, position)]


def find_reachable_keys(keys_door_dependencies: Dict[str, List[str]], collected_keys):
    """ Return list of keys that are reachable 
    
    The list of keys for which we don't have to open any door/s to get
    to them, or for which we already have the key for their door/s.
    """
    return [key for key,doors in keys_door_dependencies.items() if all(d.lower() in collected_keys for d in doors)]


def build_key_door_dependencies(
    vault_map: Dict[Tuple[int, int], str], 
    initial_position: Tuple[int, int], 
    key_positions: Dict[str, Tuple[int, int]]
) -> Dict[str, List[str]]:
    """Find all doors that need to be opened to get to each key"""
    keys_door_dependencies = {}
    for key, position in key_positions.items():
        shortest_path_key = shortest_path(vault_map, initial_position, key_positions[key])
        len_shortest_path_pairs[(initial_position, position)] = len(shortest_path_key)
        keys_door_dependencies[key] = [vault_map[pos] for pos in shortest_path_key if vault_map[pos] in string.ascii_uppercase]
    return keys_door_dependencies


def dependency_of_depedency(keys_door_dependencies, key_positions, doors_set, quadrant):
    # If key in quadrant dont  do anything
    # else substitute door for required doors for door
    substitution_dict = {}
    for door in doors_set:
        if key_in_quadrant(quadrant, key_positions[door.lower()]):
            substitution_dict[door] = door
        else:
            if len(keys_door_dependencies[door.lower()]) == 0:
                substitution_dict[door] = ''
            else:
                substitution_dict[door] = keys_door_dependencies[door.lower()]
    return substitution_dict


def build_key_door_quadrant_dependencies(
    all_key_door_dependencis,
    keys_door_dependencies:Dict[str, List[str]], 
    key_positions: Dict[int, Dict[str, List[str]]],
    quadrant: int
) -> Dict[str, List[str]]: 
    doors_set = {door for door_deps in keys_door_dependencies.values() for door in door_deps}
    print(sorted(doors_set))
    subdict = dependency_of_depedency(all_key_door_dependencis, key_positions, doors_set, quadrant)
    print(subdict)
    


def key_in_quadrant(quadrant: int, key_position: Tuple[int, int]) -> bool:
    return get_quadrant(key_position) == quadrant


def get_quadrant(position: Tuple[int, int]) -> int:
    if position[0] < 40 and position[1] < 40:
        return 1
    elif position[0] >= 40 and position[1] < 40:
        return 2
    elif position[0] < 40 and position[1] > 40:
        return 3
    else:
        return 4


def len_all_keys_shortest_path(
    vault_map: Dict[Tuple[int, int], str],
    initial_position: Tuple[int, int], 
    key_positions: Dict[str, Tuple[int, int]],
    keys_door_dependencies: Dict[str, List[str]] 
) -> List[Tuple[int, int]]:

    doors_set = set(d for deps in keys_door_dependencies.values() for d in deps )

    def heuristic(position):
        opened_doors = len([k.upper() for k in position[1] if k.upper() in doors_set])
        return (len(key_positions.keys()) - len(position[1])) + (len(doors_set) - opened_doors)

    def neighbors(position, key_positions):
        return ((key_positions[key], tuple(sorted((*position[1], key)))) for key in find_reachable_keys(keys_door_dependencies, position[1]) if key not in position[1])
        
    initial_node = (initial_position, ()) # 0 collected keys

    came_from: Dict[Tuple[int, int], List[int]] = defaultdict(list)

    # G(n) : Cost of shortest path to n 
    g_score: Dict[Tuple[int, int], int] = defaultdict(lambda: math.inf)
    g_score[initial_node] = 0

    # F(n): G(n) + h(n), where h is the heuristic function
    f_score: Dict[Tuple[int, int], int] = defaultdict(lambda: math.inf)
    f_score[initial_node] = heuristic(initial_node)

    # Initial set of visited nodes
    open_set : Set[Tuple[Tuple[int, int], Tuple[str]]] = set()
    open_set.add(initial_node)
    while open_set:
        current = min(((k,v) for k,v in f_score.items() if k in open_set), key=lambda x: x[1])[0]
        print(current, g_score[current])
        open_set.remove(current)
        if len(keys_door_dependencies.keys()) == len(current[1]):
            return build_path_backwards(current, came_from), g_score[current]
        
        for neighbor in neighbors(current, key_positions):
            cost_to_neighbor = len_shortest_path(vault_map, current[0], neighbor[0])
            if g_score[current] + cost_to_neighbor < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = g_score[current] + cost_to_neighbor
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor)
                if neighbor not in open_set:
                    open_set.add(neighbor)
    return []

    

if __name__ == '__main__':
    vault_map, initial_positions, key_positions = read_map('input2.txt')
    keys_door_dependencies = {}
    quadrant_key_positions = {}
    all_keys_door_dependencies = {}
    
    keys_door_dependencies[1] = {
        'a': [],
        'b': ['T','A','Y','Q', 'S', 'U'],
        'g': ['T','A','Y','Q', 'S', 'U', 'B'],
        'h': ['T','A','Y','Q', 'S', 'U', 'B', 'G'],
        'm': [],
        'q': ['T','A'],
        's': ['T','A', 'Y','Q'],
        't': [],
        'u': ['T','A','Y','Q', 'S'],
        'y': ['T','A']
    }
    keys_door_dependencies[2] = {
        'c': [],
        'r': [],
        'w': ['R'] # TODO" Find how to get this dependency programmatically
    }
    keys_door_dependencies[3] = {
        'f': [],
        'k': [],
        'n': []
    }
    keys_door_dependencies[4] = {
        'd': [],
        'e': ['Z', 'P'],
        'i': [],
        'j': ['Z', 'P'],
        'l': [],
        'o': ['Z', 'P', 'E', 'J', 'V'],
        'p': [],
        'v': ['Z', 'P'],
        'x': [],
        'z': []
  
    }
    total = []
    for quadrant in range(1,5):
        quadrant_map = {k:v for k,v in vault_map.items() if key_in_quadrant(quadrant, k)}
        total.append(len_all_keys_shortest_path(quadrant_map, initial_positions[quadrant-1], key_positions, keys_door_dependencies[quadrant])[1])
    print(sum(total))

