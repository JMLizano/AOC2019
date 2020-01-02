import numpy as np
import sys
import threading
sys.path.insert(0, '/home/chema/advent-of-code-2019/')
import os
import logging
logging.basicConfig(level=logging.WARNING)
import time
from typing import List, Set, Tuple, Dict
from collections import defaultdict, namedtuple
from intcode import IntcodeComputer, read_input
import queue
import copy

_INPUT_FILE='input.txt'


class NetworkComputer:
    """ Executes the given intcode program, to act as a Network computer"""

    def __init__(self, _id: int, intcode: List[int], queues: List[queue.Queue]):
        self.intcode = intcode
        self.id = _id
        self.network_address = -1
        self.queue_list = queues
        self.intcode_computer = IntcodeComputer(intcode, self.get_input, self.generate_output)
        self.next_output = 0
        self.current_incoming_packet = None
        self.current_outgoing_packet = None
        self.send_to_address = None
    
    def get_input(self):
        if self.network_address < 0:
            self.network_address = self.id
            print(f"Computer {self.id} got network adress {self.network_address}")
            return self.network_address
        if self.current_incoming_packet:
            value = self.current_incoming_packet.pop()
            print(f"Computer {self.id} getting {value} from existing packet")
            return value
        else:
            try:
                self.current_incoming_packet = self.queue_list[self.id].get_nowait()
                print(f"Computer {self.id} receiving {self.current_incoming_packet}")
                return self.current_incoming_packet.pop()
            except:
                return -1
    
    def generate_output(self, value: int):
        if self.next_output == 0:
            print(f"Computer {self.id} sending to address {value}")
            self.send_to_address = value
            self.next_output += 1
        elif self.next_output == 1:
            print(f"Computer {self.id} sending X value of {value} to address {self.send_to_address}")
            self.current_outgoing_packet = [value]
            self.next_output += 1
        elif self.next_output == 2:
            self.current_outgoing_packet.append(value)
            to_send = list(reversed(self.current_outgoing_packet))
            if self.send_to_address == 255:
                print(f"**** Got Y {value} for address 255 ****")
                for address in range(50):
                    if address != self.id:
                        self.queue_list[address].put_nowait(to_send)
            else:
                print(f"Computer {self.id} sending Y value of {value} to address {self.send_to_address}")
                self.queue_list[self.send_to_address].put_nowait(to_send)
            self.next_output = 0
    
    def execute(self):
        print(f"Computer {self.id} starting...")
        self.intcode_computer = IntcodeComputer(self.intcode, self.get_input, self.generate_output)
        self.intcode_computer.execute()


def main(intcode: List[int] = None):
    if not intcode:
        intcode = read_input(input_file=_INPUT_FILE)
    queues = [queue.Queue() for _ in range(50)]
    network_computers = []
    for network_id in range(50):
        network_computers.append(NetworkComputer(_id=network_id, intcode=copy.deepcopy(intcode), queues=queues))
    workers = [threading.Thread(target=computer.execute) for computer in network_computers]
    [worker.start() for worker in workers]
    [worker.join() for worker in workers]


if __name__ == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        intcode = [int(n) for n in sys.argv[1].split(",")]
    main(intcode)