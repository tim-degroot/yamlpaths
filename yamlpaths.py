#! /usr/bin/env python3

import scipy.constants
import yaml
import reaction_pypaths
import argparse

def gauss_get_energy(filepath, energy):
    HARTREE_TO_EV = scipy.constants.physical_constants["Hartree energy in eV"][0]
    with open(filepath) as f:
        for line in f:
            if energy in line:
                number = float(line.split()[-1])
                return number * HARTREE_TO_EV


def normalize_(values, normalize):
    if normalize:
        normalize = min(values.values())
    normalized_values = {
        key: round((value - normalize), 2) for key, value in values.items()
    }
    
    return normalized_values

def get_values(file):
    with open(file) as f:
        data = yaml.load(f, Loader=yaml.CLoader)

    file_location = data["File location"]
    energy_type = data["Energy type"]
    order = data["Diagrams"]
    values = {}

    for sub_order in order.values():
        for key, value in sub_order.items():
            if value in sub_order.keys():
                value = sub_order.get(value)
            if isinstance(value, int) or isinstance(value, float):
                values[key] = value
            else:
                full_path = f"{file_location}{value}"
                values[key] = gauss_get_energy(full_path, energy_type)

    return values, order


def yaml_path(values, order, filename, folder, normalize):
    energy_diagram = reaction_pypaths.Diagram()

    values = normalize_(values, normalize)

    levels = {}
    for mol in order:
        levels[mol] = energy_diagram.add_level(values[mol], mol)

    for i in range(len(order) - 1):
        energy_diagram.add_link(levels[order[i]], levels[order[i + 1]])

    energy_diagram.plot(f"{folder}{filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate reaction path energy diagrams from YAML",
    )
    parser.add_argument("yaml_file", type=str, help="The path to the YAML file")
    parser.add_argument(
        "-n",
        "--normalize",
        type=str,
        help="The key to normalize the values",
        default=True,
    )
    parser.add_argument("-o", "--output", type=str, help="Output directory", default="")
    args = parser.parse_args()

    values, order = get_values(args.yaml_file)
    for key, sub_order in order.items():
        yaml_path(values, list(sub_order.keys()), f"{key}.png", args.output, normalize=args.normalize)
