import logging
import sys
from part1 import total_required_fuel, module_required_fuel, read_input, _INPUT_FILE


logging.basicConfig(level=logging.INFO)


def fuel_required_for_fuel(fuel_mass) -> int:
    required_fuel = module_required_fuel(fuel_mass)
    if required_fuel <= 0:
        logging.info("Fuel mass of {} does not required further fuel".format(fuel_mass))
        return 0
    else:
        logging.info("Requiring extra {} mass of fuel for the given fuel mass of {}".format(required_fuel, fuel_mass))
        return required_fuel + fuel_required_for_fuel(fuel_mass=required_fuel)


def total_required_fuel_accounting_for_fuel(starting_mass: int = None) -> int:
    if not starting_mass:
        module_mass_list = read_input(input_file=_INPUT_FILE)
        module_fuel_requirements = (module_required_fuel(mm) for mm in module_mass_list)
    else:
        module_fuel_requirements = [module_required_fuel(starting_mass)]
    return sum(mfr + fuel_required_for_fuel(mfr) for mfr in module_fuel_requirements)


if __name__  == '__main__':
    starting_mass = 0
    if len(sys.argv) > 1:
        starting_mass = int(sys.argv[1])
    print(f"Total required fuel (taking fuel into account) is: {total_required_fuel_accounting_for_fuel(starting_mass)}")