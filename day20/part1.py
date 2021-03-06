import string
import math
from heapq import heappush, heappop
from collections import defaultdict
from typing import Dict, Tuple, List, Callable


_MOVEMENT_SET = {
    'up': (0 , -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0)
}

def get_vertical_portals(line1: int, line2: int, y_index: int):
    return {''.join(tag): (i - 2, y_index) for i,tag in enumerate(zip(line1, line2)) if tag[0] in string.ascii_uppercase}


def read_input(input_file='input.txt'):
    warp_portals = defaultdict(list)
    maze = defaultdict(lambda: ' ')
    with open(input_file, 'r') as f:
        lines = f.readlines()
        for l1,l2,y_index, m_index in ((0, 1, 0, -1), (113,114, 110, 1), (29,30, 26, 1), (84,85, 84, -1)):
            for portal, pos in get_vertical_portals(lines[l1], lines[l2], y_index).items():
                warp_portals[portal].append(pos)
                maze[(pos[0], pos[1] + m_index)] = portal

        
        for l in range(31, 84):
            for col1, col2, x_index,m_index in ((0,2,0, -1), (29,31,26,1), (82,84,82,-1), (111,113,108,1)):
                if lines[l][col1] in string.ascii_uppercase:
                    portal = ''.join(lines[l][col1:col2])
                    warp_portals[portal].append((x_index,l-2))
                    maze[(x_index + m_index, l - 2)] = portal
        
        assert all(len(pos) == 2 for portal,pos in warp_portals.items() if portal not in ('AA','ZZ'))
        
        for y in range(2, 113):
            for x,char in enumerate(lines[y]):
                if char in ('#', '.'):
                    maze[x-2, y-2] = char
        
        return maze, warp_portals


def command_line_display(maze: Dict[Tuple[int, int] ,str]):
        x,y = zip(*maze.keys())
        xmin, xmax = min(x), max(x)
        ymin, ymax = min(y), max(y)
        for y in range(ymin, ymax + 1):
            string = [f"{y:02d}"]
            for x in range(xmin, xmax + 1):
                block = maze[(x,y)]
                string.append(block[0])
            print(''.join(string))


def get_warp_position(position: Tuple[int, int], warp_portals: Dict[str, Tuple[int, int]], portal: str) -> Tuple[int, int]:
    warp_positions = warp_portals[portal]
    print(f"Getting warp position for {position} , {portal}, {warp_positions}")
    return warp_positions[1] if warp_positions[0] == position else warp_positions[0]


def neighbors(maze: Dict[Tuple[int, int] ,str], warp_portals: Dict[str, Tuple[int, int]], position: Tuple[int, int]) -> List[Tuple[int, int]]:
    neighbors_list = []
    for mov in _MOVEMENT_SET.values():
        tempative_neighbor = (position[0] + mov[0], position[1] + mov[1])
        print("temp neighbor: ", tempative_neighbor, maze[tempative_neighbor])
        if (tempative_neighbor in maze.keys() and maze[tempative_neighbor] not in ('#', ' ')):
            if maze[tempative_neighbor] in warp_portals.keys() and maze[tempative_neighbor] not in ('AA', 'ZZ'):
                neighbors_list.append(get_warp_position(position, warp_portals, maze[tempative_neighbor]))
            else:
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
    warp_portals: Dict[str, Tuple[int, int]],
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
        
        for neighbor in neighbors(search_space, warp_portals, current[1]):
            if g_score[current[1]] + 1 < g_score[neighbor]:
                came_from[neighbor] = current[1]
                g_score[neighbor] = g_score[current[1]] + 1
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, target)
                if neighbor not in open_set:
                    heappush(open_set, (f_score[neighbor], neighbor))
    return []


def search_path():
    maze,warp_portals = read_input('input.txt')
    target = (73, 0)
    initial = (35, 110)
    return a_star_search(maze, warp_portals, initial, target, lambda x,y: 0)


def do_checks():
    maze,warp_portals = read_input('input.txt')
    command_line_display(maze)
    [print(k,v) for k,v in sorted(warp_portals.items())]
    for pos in ((31, 0), (33, 26), (0, 37), (108,47)):
        print(maze[pos])
        print(neighbors(maze, warp_portals, pos))


if __name__ == '__main__':
    path = search_path()
    do_checks()
    print(f"Path len: {len(path)}")
