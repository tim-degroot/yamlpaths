<!-- [![Build Status](https://travis-ci.com/MFTabriz/reaction_pypaths.svg?branch=master)](https://travis-ci.com/MFTabriz/reaction_pypaths)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/MFTabriz/reaction_pypaths.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MFTabriz/reaction_pypaths/context:python) -->
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## reaction_pypaths

A simple yet flexible python script for drawing reaction path energy diagrams.

### Customization

All the diagram parameters can be tweaked in the [configs.py](https://github.com/tim-degroot/reaction_pypaths/blob/master/configs.py) file.
Check out the [matplotlib guide](https://matplotlib.org/tutorials/text/usetex.html) on the text rendering with LaTeX.

### Requirements

The script is written for python 3 and relies on the [matplotlib](https://matplotlib.org/) module for drawing the diagrams which in turn uses the [TeX document production system](https://tug.org/texlive/) for generating the formula/labels in the TeX format.

## yamlpaths

A command line interface (CLI) that uses [reaction_pypaths](https://github.com/MFTabriz/reaction_pypaths) to generate reaction path energy diagrams based on [YAML](https://yaml.org) files that contain energies or point to [Gaussian 16](https://gaussian.com/gaussian16/)  `.log` files.

### Installation

To be able to execute `yamlpaths.py` anywhere download the source code and make it executable and export it to `$PATH`:

```bash
chmod +x yamlpaths.py
export PATH="/path/to/PAHMC/RRKM:$PATH"
```

### Usage

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

For documentation on how to use `reaction_pypaths.py` see [MFTabriz/reaction_pypaths](https://github.com/MFTabriz/reaction_pypaths?tab=readme-ov-file#example)

### Example

```yaml
File location: /Data/Phenanthrene/DFT/C14H10-D/
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

```bash
foo@bar:~$ yamlpaths.py Deuterium.yaml
```

![Sample diagram](https://github.com/tim-degroot/reaction_pypaths/raw/master/output.png)

### License and attributions

reaction_pypaths is available under the [GNU GPL v3+](https://github.com/tim-degroot/reaction_pypaths/blob/master/LICENSE) (attribution: MFTabriz@github)
