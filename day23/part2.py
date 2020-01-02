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

    def __init__(self, _id: int, intcode: List[int], queues: List[queue.Queue], nat_queue: queue.Queue):
        self.intcode = intcode
        self.id = _id
        self.network_address = -1
        self.queue_list = queues
        self.nat_queue = nat_queue
        self.intcode_computer = IntcodeComputer(intcode, self.get_input, self.generate_output)
        self.next_output = 0
        self.current_incoming_packet = None
        self.current_outgoing_packet = None
        self.send_to_address = None
        self.waiting_input = False
    
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
                self.waiting_input = False
                return self.current_incoming_packet.pop()
            except:
                self.waiting_input = True
                return -1
    
    def generate_output(self, value: int):
        self.waiting_input = False
        if self.next_output == 0:
            self.send_to_address = value
            self.next_output += 1
        elif self.next_output == 1:
            self.current_outgoing_packet = [value]
            self.next_output += 1
        elif self.next_output == 2:
            self.current_outgoing_packet.append(value)
            to_send = list(reversed(self.current_outgoing_packet))
            if self.send_to_address == 255:
                print(f"**** Sending {to_send} to NAT ****")
                self.nat_queue.put_nowait(to_send)
            else:
                print(f"Computer {self.id} sending {to_send} to address {self.send_to_address}")
                self.queue_list[self.send_to_address].put_nowait(to_send)
            self.next_output = 0
    
    def execute(self):
        print(f"Computer {self.id} starting...")
        self.intcode_computer = IntcodeComputer(self.intcode, self.get_input, self.generate_output)
        self.intcode_computer.execute()


class NAT:
    """ Monitors the network"""
    def __init__(self, network_computers: List[NetworkComputer],input_queue: queue.Queue, queues: List[queue.Queue]):
        self.network_computers = network_computers
        self.queue_list = queues
        self.last_packet = None
        self.input_queue = input_queue
        self.last_delivered = [-1, -1]
    
    def get_last_packet(self):
        last_packet = False
        while not last_packet:
            try:
                value = self.input_queue.get_nowait()
                self.last_packet = value
            except:
                print(f"Unable to get more packets, last packet is {self.last_packet}")
                last_packet = True
    
    def restart_network(self):
        self.get_last_packet()
        print(f"### Restarting network by sending {self.last_packet} ###")
        self.queue_list[0].put(self.last_packet)
        if self.last_delivered[0] == self.last_packet[0]:
            print(f"**** Delivered {self.last_delivered[0]} twice ****")
        self.last_delivered = copy.deepcopy(self.last_packet)
        print(f"Setting last delivered to {self.last_delivered}")
    
    def all_queues_empty(self):
        return all(queue.empty() for queue in self.queue_list)
    
    def all_computers_waiting_input(self):
        return all(computer.waiting_input for computer in self.network_computers)

    def monitor(self):
        print("Starting NAT...")
        while True:
            if self.all_queues_empty() and self.all_computers_waiting_input():
                time.sleep(5)
                if self.all_queues_empty() and self.all_computers_waiting_input():
                    print("Restarting network...")
                    self.restart_network()
            time.sleep(1)


def main(intcode: List[int] = None):
    if not intcode:
        intcode = read_input(input_file=_INPUT_FILE)
    
    queues = [queue.Queue() for _ in range(50)]
    nat_queue = queue.Queue()
    network_computers = []
    for network_id in range(50):
        network_computers.append(NetworkComputer(_id=network_id, intcode=copy.deepcopy(intcode), queues=queues, nat_queue=nat_queue))
    nat = NAT(network_computers, nat_queue, queues)
    workers = [threading.Thread(target=computer.execute) for computer in network_computers]
    workers.append(threading.Thread(target=nat.monitor))
    [worker.start() for worker in workers]
    [worker.join() for worker in workers]


if __name__ == '__main__':
    intcode = None
    if len(sys.argv) > 1:
        intcode = [int(n) for n in sys.argv[1].split(",")]
    main(intcode)