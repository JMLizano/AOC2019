import string
import math
from heapq import heappush, heappop
from collections import defaultdict
from typing import Dict, Tuple, List, Callable, Set


_MOVEMENT_SET = {
    'up': (0 , -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0)
}

def get_vertical_portals(line1: int, line2: int, y_index: int):
    return {''.join(tag): (i - 2, y_index) for i,tag in enumerate(zip(line1, line2)) if tag[0] in string.ascii_uppercase}

def read_input_test(input_file='test.txt'):
    warp_portals = defaultdict(list)
    maze = defaultdict(lambda: ' ')
    with open(input_file, 'r') as f:
        lines = f.readlines()
        for l1,l2,y_index, m_index in ((0, 1, 0, -1), (35,36, 32, 1), (9,10, 6, 1), (26,27, 26, -1)):
            for portal, pos in get_vertical_portals(lines[l1], lines[l2], y_index).items():
                warp_portals[portal].append(pos)
                maze[(pos[0], pos[1] + m_index)] = portal

        
        for l in range(8, 28):
            for col1, col2, x_index,m_index in ((0,2,0, -1), (9,11,6,1), (34,36,34,-1), (43,45,40,1)):
                if lines[l][col1] in string.ascii_uppercase:
                    portal = ''.join(lines[l][col1:col2])
                    warp_portals[portal].append((x_index,l-2))
                    maze[(x_index + m_index, l - 2)] = portal

        assert all(len(pos) == 2 for portal,pos in warp_portals.items() if portal not in ('AA','ZZ'))
        
        for y in range(2, 35):
            for x,char in enumerate(lines[y]):
                if char in ('#', '.'):
                    maze[x-2, y-2] = char
        
        return maze, warp_portals

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
    return warp_positions[1] if warp_positions[0] == position else warp_positions[0]


def neighbors(maze: Dict[Tuple[int, int] ,str], warp_portals: Dict[str, Tuple[int, int]], position: Tuple[int, int], level: int) -> List[Tuple[int, int]]:
    neighbors_list = []
    for mov in _MOVEMENT_SET.values():
        tempative_neighbor = (position[0] + mov[0], position[1] + mov[1])
        if (tempative_neighbor in maze.keys() and maze[tempative_neighbor] not in ('#', ' ')):
            if maze[tempative_neighbor] in warp_portals.keys() and maze[tempative_neighbor] not in ('AA', 'ZZ'):
                if level > 0 and (position[0] < 26 or position[0] > 82 or  position[1] > 84 or position[1] < 26): 
                # if level > 0 and (position[0] < 6 or position[0] > 34 or position[1] > 26 or position[1] < 6): 
                    # At the outer level, only inner portals work
                    # print(f"{position}, {level}: going up")
                    neighbors_list.append((level - 1, get_warp_position(position, warp_portals, maze[tempative_neighbor])))
                elif position[0] >= 26 and position[0] <= 82 and position[1] >= 26 and position[1] <= 84:
                    # print(f"{position}, {level}: going down")
                    neighbors_list.append((level + 1, get_warp_position(position, warp_portals, maze[tempative_neighbor])))
            else:
                neighbors_list.append((level,tempative_neighbor))
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


def level_heuristic(current: Tuple[int, Tuple[int, int]], target: Tuple[int, Tuple[int, int]]) -> int:
    value = math.sqrt((target[1][0] - current[1][0]) ** 2 + (target[1][1] - current[1][1]) ** 2) + (10 * abs(target[0] - current[0]))
    return value


def a_star_search(
    search_space: Dict[Tuple[int, int], str],
    warp_portals: Dict[str, Tuple[int, int]],
    initial_position: Tuple[int, int], 
    target: Tuple[int, int], 
    heuristic: Callable
) -> List[Tuple[int, int]]:

    came_from: Dict[Tuple[int, Tuple[int, int]], List[int]] = defaultdict(list)

    # Node: (level, Position(x,y))
    # G(n) : Cost of shortest path to n 
    g_score: Dict[Tuple[int, Tuple[int, int]], int] = defaultdict(lambda: math.inf)
    g_score[initial_position] = 0

    # F(n): G(n) + h(n), where h is the heuristic function
    f_score: Dict[Tuple[int, Tuple[int, int]], int] = defaultdict(lambda: math.inf)
    f_score[initial_position] = heuristic(initial_position, target)

    # Initial set of visited nodes
    open_set : Set[Tuple[int, Tuple[int, int]]] = set()
    open_set_heap: List[Tuple[int, Tuple[int, int]]] = []
    open_set.add(initial_position)
    heappush(open_set_heap, (f_score[initial_position], initial_position))
    while open_set:
        # current = min(((k,v) for k,v in f_score.items() if k in open_set), key=lambda x: x[1])[0]
        current = heappop(open_set_heap)[1]
        open_set.remove(current)
        print(len(open_set))
        if current == target:
            return build_path_backwards(current, came_from)
        
        for neighbor in neighbors(search_space, warp_portals, current[1], current[0]):
            if g_score[current] + 1 < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = g_score[current] + 1
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, target)
                if neighbor not in open_set:
                    open_set.add(neighbor)
                    heappush(open_set_heap, (f_score[neighbor], neighbor))
    return []


def search_path():
    maze,warp_portals = read_input('input.txt')
    command_line_display(maze)
    target = (0, (73, 0))
    initial = (0, (35, 110))
    print(maze[(73, 0)])
    print(maze[(73, -1)])
    print(maze[(35, 110)])
    print(maze[(35, 111)])
    return a_star_search(maze, warp_portals, initial, target, level_heuristic)


def do_checks():
    maze,warp_portals = read_input('input.txt')
    command_line_display(maze)
    [print(k,v) for k,v in sorted(warp_portals.items())]
    for pos in ((31, 0), (33, 26), (0, 37), (108,47)):
        print(maze[pos])
        print(neighbors(maze, warp_portals, pos, 0))

def test():
    maze,warp_portals = read_input_test('test.txt')
    command_line_display(maze)
    target = (0, (11, 0))
    initial = (0, (13, 32))
    print(maze[(11, 0)])
    print(maze[(11, -1)])
    print(maze[(13, 32)])
    print(maze[(13, 33)])
    return a_star_search(maze, warp_portals, initial, target, level_heuristic)

if __name__ == '__main__':
    # path = test()
    # print(path)
    # print(f"Test path len: {len(path)}")
    path = search_path()
    print(path)
    print(f"Path len: {len(path)}")
