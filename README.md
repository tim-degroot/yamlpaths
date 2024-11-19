# yamlpaths: Simple and beautiful reaction path energy diagrams

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](http://python.org)
[![YAML](https://img.shields.io/badge/YAML-CB171E?logo=yaml&logoColor=fff)](http://yaml.org)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

yamlpaths is a command line interface (CLI) based on  [reaction_pypaths](https://github.com/MFTabriz/reaction_pypaths) that generates reaction path energy diagrams based on [YAML](https://yaml.org) files that contain energies or point to [Gaussian 16](https://gaussian.com/gaussian16/)  `.log` files.

## Installation

To be able to execute `yamlpaths.py` anywhere download the source code and make it executable and export it to `$PATH`:

```bash
chmod +x yamlpaths.py
export PATH="/path/to/PAHMC/RRKM:$PATH"
```

## Usage

Create a YAML file containg the following:

```yaml
File location: /path/to/gaussian/output/
Energy type: Sum of electronic and zero-point Energies 
Diagrams: 
  title:
    x: x.log
    y: 1.5
    z: x 
```

The program will create all Diagrams as `title.png` which contains a diagram of the reaction along the path `x > y > z`. The values can be set as `int` or `float` numbers or they will be gathered using the  `Energy type` from the  Gaussian `.log` files. The program can use aliases to use the energy of another state in case of symmetries `z: x`.

```bash
usage: yamlpaths.py [-h] [-n NORMALIZE] [-o OUTPUT] yaml_file

Generate reaction path energy diagrams from YAML

positional arguments:
  yaml_file             The path to the YAML file

options:
  -h, --help            show this help message and exit
  -n, --normalize NORMALIZE
                        The key to normalize the values
  -o, --output OUTPUT   Output directory
```

For documentation on how to use `reaction_pypaths.py` and `config.py` see [MFTabriz/reaction_pypaths](https://github.com/MFTabriz/reaction_pypaths?tab=readme-ov-file#example)

### Example using values

```yaml
Diagrams:
  Anthracene:
    D9: 0.00
    D9to9a: 1.35
    D9a: 1.32
    D9ato1: 1.57
    D1: 0.42
    D1to2: 1.06
    D2: 0.50
```

![Sample diagram for Anthracene](https://github.com/tim-degroot/reaction_pypaths/raw/master/Anthracene.png)

### Example using Gaussian

```yaml
File location: /Data/Phenanthrene/DFT/
Energy type: Sum of electronic and zero-point Energies
Diagrams:
  D9toD1:
    D9: D10
    D9to10: C14H10-D9to10.log
    D10: C14H10-D10.log
    D10to10a: C14H10-D10to10a.log
    D10a: C14H10-D10a.log
    D1to10a: C14H10-D1to10a.log
    D1: C14H10-D1.log
```

![Sample diagram for Phenanthrene D9-D1](https://github.com/tim-degroot/reaction_pypaths/raw/master/output.png)

### License and attributions

yamlpaths is available under the [GNU GPL v3+](https://github.com/tim-degroot/reaction_pypaths/blob/master/LICENSE) (attribution: MFTabriz@github, tim-degroot@github)
