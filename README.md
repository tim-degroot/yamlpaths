<!-- [![Build Status](https://travis-ci.com/MFTabriz/reaction_pypaths.svg?branch=master)](https://travis-ci.com/MFTabriz/reaction_pypaths)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/MFTabriz/reaction_pypaths.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MFTabriz/reaction_pypaths/context:python) -->
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## reaction_pypaths

A simple yet flexible python script for drawing reaction path energy diagrams.

### Customization

All the diagram parameters can be tweaked in the [configs.py](https://github.com/MFTabriz/reaction_pypaths/blob/master/configs.py) file.
Check out the [matplotlib guide](https://matplotlib.org/tutorials/text/usetex.html) on the text rendering with LaTeX.

### Requirements

The script is written for python 3 and relies on the [matplotlib](https://matplotlib.org/) module for drawing the diagrams which in turn uses the [TeX document production system](https://tug.org/texlive/) for generating the formula/labels in the TeX format.

### yamlpaths

A command line interface (CLI) that interfaces with reaction_pypaths to generate reaction path energy diagrams based on [YAML](https://yaml.org) files.

### Example

Create a YAML file such as the following `Deuterium.yaml`:

```yaml
File location: /Phenanthrene/DFT/
TS location: /DFT/TS/
File prefix: C14H10-
File suffix: .log
Diagrams:
  D9toD1:
    D9: D10
    D9to10: 
    D10: 
    D10to10a: 
    D10a: 
    D1to10a: 
    D1: 
```

Execute the program:

```bash
yamlpaths.py Deuterium.yaml
```

![Sample diagram](https://github.com/MFTabriz/reaction_pypaths/raw/master/output.png)

### Usage

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

### License and attributions

reaction_pypaths is available under the [GNU GPL v3+](https://github.com/tim-degroot/reaction_pypaths/blob/master/LICENSE) (attribution: MFTabriz@github)
