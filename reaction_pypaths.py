"""
reaction_pypaths
A simple python script for drawing the reaction path energy diagrams

Author: MFTabriz@github
License: GPL v3+

See example.py for a simple example of the usage
"""

import sys
from collections import namedtuple

from matplotlib import pyplot as plt
from matplotlib import rc, use
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D as line
from matplotlib.path import Path
from matplotlib.textpath import TextToPath

import configs

use("AGG")

Level = namedtuple(
    "Level",
    [
        "order",
        "energy",
        "label",
        "energy_tag_color",
        "label_color",
        "line_color",
        "width",
        "start_position",
    ],
)

Link = namedtuple("Link", ["level_id1", "level_id2", "color", "width", "style"])


class Diagram:
    def __init__(self):
        rc("font", **{"serif": [configs.plot_font]})
        rc("text", usetex=True)
        self.levels = []
        self.links = []

    def add_level(
        self,
        energy,
        label,
        attach_last=False,
        energy_tag_color=None,
        label_color=None,
        line_color=None,
    ):
        """
        Add a new level to the diagram
            energy : Energy of the new level
            label : tag for the new level
            attach_last: True [the level should be grouped with the last level]
            label_color
            line_color

        Returns the ID of the new level
        """
        if self.levels:
            last_order = self.levels[-1].order
            if attach_last:
                level_order = last_order
            else:
                level_order = last_order + 1
        else:
            level_order = 0

        fp = FontProperties(
            family=configs.plot_font, size=configs.level_labels_fontsize
        )
        pathgenerator = TextToPath()
        pathgenerator.DPI = configs.plot_dpi
        verts, codes = pathgenerator.get_text_path(fp, label, ismath="TeX")
        text_size = Path(verts, codes).get_extents()
        level_width = (
            text_size.width / configs.plot_dpi * 1.5 + configs.level_labels_padding
        )

        if not energy_tag_color:
            energy_tag_color = configs.energy_tags_color

        if not label_color:
            label_color = configs.level_labels_color

        if not line_color:
            line_color = configs.level_lines_color

        start_position = None
        level_id = len(self.levels)

        self.levels.append(
            Level(
                level_order,
                energy,
                label,
                energy_tag_color,
                label_color,
                line_color,
                level_width,
                start_position,
            )
        )

        return level_id

    def add_link(self, level_id1, level_id2, color=None, width=None, style=None):
        """
        Add a new link to the diagram
            level_id1, level_id2 : ID of the connecting levels
            color
            width
            style
        """
        if max(level_id1, level_id2) >= len(self.levels):
            sys.exit("ERROR: invalid level_id for linking!")
        if not color:
            color = configs.links_color
        if not width:
            width = configs.links_width
        if not style:
            style = configs.links_style
        self.links.append(Link(level_id1, level_id2, color, width, style))

    def plot(self, output_file, ylim=None):
        """
        plot the diagram
        ylim : tuple (y_min, y_max) to set custom y-axis limits
        """
        self._adjust_positions()

        figure = plt.figure(
            figsize=[configs.plot_width, configs.plot_height], dpi=configs.plot_dpi
        )
        diag = figure.add_subplot(1, 1, 1, xmargin=0.02, ymargin=0.02)
        diag.set_ylabel(
            configs.energy_axis_label,
            fontweight=configs.energy_axis_label_fontweight,
            size=configs.energy_axis_label_fontsize,
        )
        diag.axes.get_xaxis().set_visible(False)
        diag.axes.tick_params(
            width=configs.energy_axis_ticks_width,
            length=configs.energy_axis_ticks_length,
            labelsize=configs.energy_axis_ticks_fontsize,
        )
        diag.spines["top"].set_visible(False)
        diag.spines["right"].set_visible(False)
        diag.spines["bottom"].set_visible(False)

        # plot levels
        for level_id, level in enumerate(self.levels):
            diag.hlines(
                level.energy,
                level.start_position,
                level.start_position + level.width,
                colors=level.line_color,
                linewidth=configs.level_lines_thickness,
            )
            if level.energy == 0:
                energy_label = "0"
            else:
                energy_label = "{0:+}".format(level.energy)

            diag.text(
                level.start_position + level.width / 2,
                level.energy + configs.energy_tags_offset,
                energy_label,
                horizontalalignment="center",
                verticalalignment="bottom",
                size=configs.energy_tags_fontsize,
                color=configs.energy_tags_color,
                fontweight=configs.energy_tags_fontweight,
            )

            diag.text(
                level.start_position + level.width / 2,
                level.energy - configs.level_labels_offset,
                level.label,
                horizontalalignment="center",
                verticalalignment="top",
                size=configs.level_labels_fontsize,
                color=configs.level_labels_color,
                fontweight=configs.level_labels_fontweight,
            )

            # plot links
            for link_idx, link in enumerate(self.links):
                left_level_id = min(link.level_id1, link.level_id2)
                right_level_id = max(link.level_id1, link.level_id2)
                x1 = (
                    self.levels[left_level_id].start_position
                    + self.levels[left_level_id].width
                )
                x2 = self.levels[right_level_id].start_position
                y1 = self.levels[left_level_id].energy
                y2 = self.levels[right_level_id].energy
                link_line = line(
                    [x1, x2],
                    [y1, y2],
                    linestyle=link.style,
                    linewidth=link.width,
                    color=link.color,
                )
                diag.add_line(link_line)

                min_energy = min(level.energy for level in self.levels)
                max_energy = max(level.energy for level in self.levels)
                if ylim:
                    y_min, y_max = ylim
                else:
                    y_min = min(min_energy * 1.1, min_energy * 0.9)
                    y_max = max(max_energy * 1.1, max_energy * 0.9)
                plt.ylim(y_min, y_max)

        if not output_file:
            output_file = "output.png"
        figure.savefig(output_file, dpi=configs.plot_dpi)

    def _adjust_positions(self):
        """
        Adjust the parameters for the width of the diagram and tag offsets
        """
        distinct_levels_num = self.levels[-1].order + 1
        next_level_start_position = configs.levels_horizontal_offset

        for level_order in range(0, distinct_levels_num):
            widest = max(
                [
                    level.width if level.order == level_order else 0
                    for level in self.levels
                ]
            )

            for level_id, level in enumerate(self.levels):
                if level.order == level_order:
                    multi_level_adjustment = (widest - level.width) / 2
                    self.levels[level_id] = self.levels[level_id]._replace(
                        start_position=next_level_start_position
                        + multi_level_adjustment
                    )

            next_level_start_position += widest + configs.levels_horizontal_offset

        configs.plot_width = next_level_start_position / 10
        min_energy = min(level.energy for level in self.levels)
        max_energy = max(level.energy for level in self.levels)
        energy_range = max_energy - min_energy

        configs.level_labels_offset *= energy_range / configs.plot_height
        configs.energy_tags_offset *= energy_range / configs.plot_height
