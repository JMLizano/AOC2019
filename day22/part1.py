import re
from typing import List, Tuple


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
                print(f"Deal with increment {operation[1]}")
                stack = deal_w_increment(stack, operation[1])
            else:
                print(f"Deal new stack")
                stack = deal_new_stack(stack)
        elif operation[0] == 'cut':
            print(f"Cut {operation[1]}")
            stack = cut(stack, operation[1])
        else:
            raise(f"Invalid operation {operation[0]}")
    return stack


def test():
    operations = read_input('test.txt')
    new_stack = do_shuffling(list(range(10)), operations)
    print(new_stack)


if __name__ == '__main__':
    # test()
    operations = read_input()
    new_stack = do_shuffling(list(range(10007)), operations)
    print(f"Position of card 2019: {new_stack.index(2019)}")