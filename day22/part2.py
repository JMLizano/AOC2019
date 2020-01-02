import re
import sys
import pandas as pd
from typing import List, Tuple, Dict
from collections import namedtuple


lcf = namedtuple('lcf', ['a', 'b'])


def read_input(input_file='input.txt') -> List[Tuple[str, int]]:
    search_numbers = re.compile(r'.\d+')
    result = []
    with open(input_file, 'r') as f:
        for line in  f.readlines():
            number = search_numbers.findall(line)
            number = int(number[0]) if len(number) > 0 else None
            result.append((line.split(' ')[0], number))
    return result


def deal_new_stack(stack: List[int]) -> List[int]:
    return list(reversed(stack))


def deal_w_increment(stack: List[int], increment: int) -> List[int]:
    new_stack = [0] * len(stack)
    current_pos = 0
    for card in stack:
        new_stack[current_pos % len(new_stack)] = card
        current_pos += increment
    return new_stack


def cut(stack: List[int], to_cut: int) -> List[int]:
    if to_cut < 0:
        return stack[to_cut:] + stack[:to_cut]
    else:
        return stack[to_cut:] + stack[:to_cut]


def do_shuffling(stack: List[int], operations: List[str]):
    for operation in operations:
        if operation[0] == 'deal':
            if operation[1]:
                stack = deal_w_increment(stack, operation[1])
            else:
                stack = deal_new_stack(stack)
        elif operation[0] == 'cut':
            stack = cut(stack, operation[1])
        else:
            raise(f"Invalid operation {operation[0]}")
    return stack

def compose_lcf(first, second, modulo):
    return lcf((first.a * second.a) % modulo, (first.b * second.a + second.b) % modulo)


def build_lcf(operations, deck_size):
    """ Build linear congruent function that represents the whole shuffle"""
    lcf_expression = None
    for operation in operations:
        if operation[0] == 'deal':
            if operation[1]:
                current_lcf = lcf(operation[1], 0)
            else:
                current_lcf = lcf(-1, -1)
        elif operation[0] == 'cut':
             current_lcf = lcf(1, -operation[1])
        else:
            raise(f"Invalid operation {operation[0]}")
        if lcf_expression:
            lcf_expression = compose_lcf(lcf_expression, current_lcf, deck_size)
        else:
            lcf_expression = current_lcf
    return lcf_expression


def pow_mod(x, n, m):
    if n == 0: return 1
    if n % 2 == 0:
        t = pow_mod(x, n/2, m)
        return (t * t)  % m
    else:
        t = pow_mod(x, (n-1)/2, m)
        return (t * t * x)  % m

def multiplicative_inverse(x, m):
    return pow_mod(x, m - 2, m)

def compose_k_times(lcf_expression, k, deck_size):
    a_k = pow_mod(lcf_expression.a,  k, deck_size)
    numerator = lcf_expression.b * (1 - a_k)
    denominator = 1 - lcf_expression.a 
    b = ( numerator * multiplicative_inverse(denominator, deck_size) ) % deck_size
    return lcf(a_k, b)

def find_card_in_index(lcf_expression, index, deck_size):
    return ( (index - lcf_expression.b ) * multiplicative_inverse(lcf_expression.a , deck_size) ) % deck_size

def find_shuffle_positions(stack: List[int], new_stack: List[int]) -> Dict[int, int]:
    return {i: stack.index(v) for i,v in enumerate(new_stack) }


def shuffle_with_dict(stack: List[int], shuffle_dict: Dict[int, int]):
    return [stack[v] for i,v in sorted(shuffle_dict.items())]


def shuffle_repeated(stack, shuffle_dict):
    positions = set()
    print(f"Initial position: {stack.index(2020)}")
    positions.add(stack.index(2020))
    for i in range(10000):
        stack = shuffle_with_dict(stack, shuffle_dict)
        new_position = stack.index(2020)
        # print(new_position)
        if new_position in positions:
            print(f"Repeated {new_position} after {i} iterations")
            break
        positions.add(new_position)
    return stack

def shuffle_repeated2(stack, shuffle_dict):
    values = set()
    print(f"Initial value: {stack[2020]}")
    values.add(stack[2020])
    for i in range(10000):
        stack = shuffle_with_dict(stack, shuffle_dict)    
        new_value = stack[2020]
        if new_value in values:
            print(f"Repeated {new_value} after {i} iterations")
            break
        values.add(new_value)
    return stack


def test():
    operations = read_input()
    deck_size = int(sys.argv[1])
    lcf = build_lcf(operations, deck_size)
    print(lcf)
    print(compose_k_times(lcf, 1, deck_size))
    assert lcf == compose_k_times(lcf, 1, deck_size)


def main():
    operations = read_input()
    deck_size = int(sys.argv[1])
    lcf = build_lcf(operations, deck_size)
    lcf_k = compose_k_times(lcf, 101741582076661, deck_size)
    print(find_card_in_index(lcf_k, 2020, deck_size))

if __name__ == '__main__':
    main()
    
    
    