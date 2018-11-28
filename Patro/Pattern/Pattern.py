####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2017 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import logging

from IntervalArithmetic import Interval2D

from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicEngine.GraphicScene.GraphicItem import GraphicStyle
from Patro.GraphicEngine.GraphicScene.Scene import GraphicScene
from . import Calculation
from .Calculator import Calculator

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Pattern:

    _logger = _module_logger.getChild('Pattern')

    ##############################################

    def __init__(self, measurements, unit):

        self._measurements = measurements
        self._calculator = Calculator(self._measurements)
        self._calculations = []
        self._calculation_dict = {}
        self._unit = unit

    ##############################################

    @property
    def measurements(self):
        return self._measurements

    @property
    def calculator(self):
        return self._calculator

    @property
    def unit(self):
        return self._unit

    ##############################################

    @property
    def calculations(self):
        return self._calculations

    ##############################################

    def _add_calculation(self, calculation):

        # Works as a post init
        self._calculations.append(calculation)
        self._calculation_dict[calculation.id] = calculation
        if hasattr(calculation, 'name'):
            self._calculation_dict[calculation.name] = calculation

    ##############################################

    def get_calculation_id(self):
        return len(self._calculations) + 1 # id > 0

    ##############################################

    def has_calculation_id(self, id):
        return id in self._calculation_dict

    ##############################################

    def get_calculation(self, id):
        return self._calculation_dict[id]

    ##############################################

    def get_point(self, name):
        return self._points[name]

    ##############################################

    def eval(self):

        self._logger.info('Eval all calculations')
        for calculation in self._calculations:
            if isinstance(calculation, Calculation.Point):
                self._calculator.add_point(calculation)
                calculation.eval()
            elif isinstance(calculation, Calculation.SimpleInteractiveSpline):
                calculation.eval() # for control points
            else:
                pass
            calculation.connect_ancestor_for_expressions()

    ##############################################

    def dump(self):

        print("\nDump calculations:")
        for calculation in self._calculations:
            if isinstance(calculation, Calculation.Point):
                print(calculation, calculation.vector)
            else:
                print(calculation)
            for dependency in calculation.dependencies:
                print('  ->', dependency)

    ##############################################

    @property
    def bounding_box(self):

        """Compute the bounding box of the pattern."""

        # Fixme: to function
        bounding_box = None
        for calculation in self._calculations:
            interval = calculation.geometry().bounding_box
            # print(calculation.geometry(), interval)
            if bounding_box is None:
                bounding_box = interval
            else:
                bounding_box |= interval

        return bounding_box

    ##############################################

    def _calculation_to_path_style(self, calculation, **kwargs):

        return GraphicStyle(
            stroke_style=calculation.line_style,
            stroke_color=calculation.line_color,
            **kwargs
        )

    ##############################################

    def detail_scene(self, scene_cls=GraphicScene):

        """Generate a graphic scene for the detail mode"""

        scene = scene_cls()
        # Fixme: scene bounding box
        scene.bounding_box = self.bounding_box

        # Fixme: implement a transformer class to prevent if ... ?

        for calculation in self._calculations:

            if isinstance(calculation, Calculation.Point):
                scene.add_coordinate(calculation.name, calculation.vector)
                scene.circle(calculation.name, '1pt', GraphicStyle(fill_color='black'),
                             user_data=calculation)
                label_offset = calculation.label_offset
                offset = Vector2D(label_offset.x, -label_offset.y) # Fixme: ???
                label_position = calculation.vector + offset
                if offset:
                    # arrow must point to the label center and be clipped
                    scene.segment(calculation.vector, label_position, GraphicStyle(line_width='.5pt'),
                                  user_data=calculation)
                    scene.text(label_position, calculation.name, user_data=calculation)

                if isinstance(calculation, Calculation.LinePropertiesMixin):
                    path_style = self._calculation_to_path_style(calculation, line_width='2pt')
                    if isinstance(calculation, Calculation.AlongLinePoint):
                        scene.segment(calculation.first_point.name, calculation.name, path_style,
                                      user_data=calculation)
                    elif isinstance(calculation, Calculation.EndLinePoint):
                        scene.segment(calculation.base_point.name, calculation.name, path_style,
                                      user_data=calculation)
                    # elif isinstance(calculation, LineIntersectPoint):
                    #     scene.segment(calculation.point1_line1.name, calculation.name, path_style)
                    #     source += r'\draw[{0}] ({1.point1_line1.name}) -- ({1.name});'.format(style, calculation) + '\n'
                    elif isinstance(calculation, Calculation.NormalPoint):
                        scene.segment(calculation.first_point.name, calculation.name, path_style,
                                      user_data=calculation)

            elif isinstance(calculation, Calculation.Line):
                path_style = self._calculation_to_path_style(calculation, line_width='4pt')
                scene.segment(calculation.first_point.name, calculation.second_point.name, path_style,
                              user_data=calculation)

            elif isinstance(calculation, Calculation.SimpleInteractiveSpline):
                path_style = self._calculation_to_path_style(calculation, line_width='4pt')
                scene.cubic_bezier(calculation.first_point.name,
                                   calculation.control_point1, calculation.control_point2,
                                   calculation.second_point.name,
                                   path_style,
                                   user_data=calculation,
                )

        return scene

