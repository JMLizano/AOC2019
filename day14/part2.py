import math
import sys
import logging
from typing import List, Tuple
from collections import namedtuple, defaultdict


logging.basicConfig(level=logging.WARNING)


_INPUT_FILE = 'input.txt'


def get_material(material_str: str) -> Tuple[str, int]:
    mat_and_amount = material_str.strip().split(' ')
    return mat_and_amount[1], int(mat_and_amount[0])



def read_input(input_file: str) -> List[int]:
    materials_dictionary = {}
    with open(file=input_file, mode='r') as f:
        # Read each line.
        # For each line get inputs and output
        # For each input get (MAT, AMOUNT)
        # Add to dict[MAT] -> (AMOUN, [INPUTS])
        lines = [l.rstrip() for l in f.readlines()]
        for l in lines:
            input_output = [m.strip() for m in  l.split('=>')]
            output = get_material(input_output[1])
            inputs = [get_material(mat) for mat in input_output[0].strip().split(',') if mat !='']
            materials_dictionary[output[0]] = (output[1], inputs)
        return materials_dictionary


def get_raw_materials(element, required_amount, mats, excedent, raw_materials, excedent_raw_materials):
    required_mats = mats[element][1] # List of required mats
    logging.info(f"Getting required fuel for {required_amount} of {element} with {excedent[element]} excedent")
    if required_mats[0][0] != 'ORE': 
        required_amount -= excedent[element]
        times_recipe_required = math.ceil(required_amount / mats[element][0])
        current_excedent = (times_recipe_required * mats[element][0]) - required_amount
        excedent[element] = current_excedent
        logging.info(f"Setting excedent for {element} to {current_excedent}")
    else:
        excedent_raw_materials[element] += required_amount % mats[element][0]
    for mat in required_mats:
        if mat[0] == 'ORE':
            logging.info(f"Adding {required_amount} of {element}")
            raw_materials[element] += required_amount
        else:
            raw_materials, excedent, excedent_raw_materials = get_raw_materials(mat[0], times_recipe_required * mat[1], mats, excedent, raw_materials, excedent_raw_materials)
    return raw_materials, excedent, excedent_raw_materials


def search_fuel_target(mats, ore):
    one_unit = get_required_ore(mats, 1)
    target = ore//one_unit
    used_ore = get_required_ore(mats, target)
    while True:
        target += (ore-used_ore)//one_unit + 1
        used_ore = get_required_ore(mats, target)
        if used_ore > ore:
            break
    return target - 1


def get_required_ore(mats, target):
    required_raw_materials, excedent, excedent_raw_materials= get_raw_materials('FUEL', target, mats, defaultdict(int), defaultdict(int), defaultdict(int))
    print(excedent_raw_materials)
    logging.info(f"Total required raw materials: {required_raw_materials}")
    total_ore = 0
    for rm, amount in required_raw_materials.items():
        times_recipe_required = math.ceil((amount + excedent[rm]) / mats[rm][0])
        total_ore += times_recipe_required * mats[rm][1][0][1]
    return total_ore


if __name__ == '__main__':
    if len(sys.argv) > 1:
        _INPUT_FILE = sys.argv[1]
    print(f"Maximum fuel: {search_fuel_target(read_input(_INPUT_FILE), 1000000000000)}")