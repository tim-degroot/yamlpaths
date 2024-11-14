#! /usr/bin/env python3

import scipy.constants
import yaml
import reaction_pypaths
import argparse

def plot(file, normalize=None, folder=''):
    values, order = get_values(file, normalize=normalize)
    for key, sub_order in order.items():
        yaml_path(values, list(sub_order.keys()), f'{key}.png', folder)

def gauss_get_energy(filepath, energy='Sum of electronic and zero-point Energies'):
    HARTREE_TO_EV = scipy.constants.physical_constants['Hartree energy in eV'][0]
    with open(filepath) as f:
        for line in f:
            if energy in line:
                number = float(line.split()[-1])
                return number * HARTREE_TO_EV

def get_values(file, normalize):
    with open(file) as f:
        data = yaml.load(f, Loader=yaml.CLoader)

    file_location = data['File location']
    ts_location = data['TS location']
    file_prefix = data['File prefix']
    file_suffix = data['File suffix']
    order = data['Diagrams']
    values = {}

    for sub_order in order.values():
        for key, value in sub_order.items():
            full_path = f''
            full_path += ts_location if 'to' in key else file_location
            full_path += file_prefix
            full_path += key if value is None else value
            full_path += file_suffix
            
            values[key] = gauss_get_energy(full_path)

    normalized_values = {key: round((value - values.get(normalize, min(values.values()))), 2) for key, value in values.items()}
    return normalized_values, order

def yaml_path(values, order, filename, folder):
    energy_diagram = reaction_pypaths.Diagram()

    levels = {}
    for mol in order:
        levels[mol] = energy_diagram.add_level(values[mol], mol)

    # Add links between the levels
    for i in range(len(order) - 1):
        energy_diagram.add_link(levels[order[i]], levels[order[i + 1]])

    # Plot the diagram and save the final result to the file
    energy_diagram.plot(f'{folder}{filename}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate reaction path energy diagrams from YAML')
    parser.add_argument('yaml_file', type=str, help='The path to the YAML file')
    parser.add_argument('-n', '--normalize', type=str, help='The key to normalize the values', default=None)
    parser.add_argument('-o', '--output', type=str, help='Output directory', default='')
    args = parser.parse_args()

    values, order = get_values(args.yaml_file, normalize=args.normalize)
    for key, sub_order in order.items():
        yaml_path(values, list(sub_order.keys()), f'{key}.png', args.o)