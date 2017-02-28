####################################################################################################
#
# PyValentina - A Python implementation of Valentina Pattern Drafting Software
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

from Valentina.Geometry.Transformation import AffineTransformation2D
from .GraphicItem import CoordinateItem, TextItem, CircleItem, SegmentItem, CubicBezierItem

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class GraphicSceneScope:

    ##############################################

    def __init__(self, transformation=None):

        if transformation is None:
            transformation = AffineTransformation2D.Identity()
        self._transformation = transformation
        self._items = []

    ##############################################

    @property
    def transformation(self):
        return self._transformation

    # @transformation.setter
    # def transformation(self, value):
    #     self._transformation = value

    ##############################################

    def __iter__(self):

        return iter(self._items)

    ##############################################

    def _add_item(self, cls, *args, **kwargs):

        item = cls(*args, **kwargs)
        self._items.append(item)
        return item

    ##############################################

    def add_scope(self, *args, **kwargs):
        return self._add_item(GraphicSceneScope, self, *args, **kwargs)

    def add_coordinate(self, *args, **kwargs):
        return self._add_item(CoordinateItem, *args, **kwargs)

    def add_text(self, *args, **kwargs):
        return self._add_item(TextItem, *args, **kwargs)

    def add_segment(self, *args, **kwargs):
        return self._add_item(SegmentItem, *args, **kwargs)

    def add_circle(self, *args, **kwargs):
        return self._add_item(CircleItem, *args, **kwargs)

    def add_cubic_bezier(self, *args, **kwargs):
        return self._add_item(CubicBezierItem, *args, **kwargs)

####################################################################################################

class GraphicScene:

    ##############################################

    def __init__(self):

        self._root_scope = GraphicSceneScope()

    ##############################################

    @property
    def root_scope(self):
        return self._root_scope

    ##############################################

    def add_scope(self, *args, **kwargs):
        return self._root_scope.add_scope(*args, **kwargs)

    def add_coordinate(self, *args, **kwargs):
        return self._root_scope.add_coordinate(*args, **kwargs)

    def add_text(self, *args, **kwargs):
        return self._root_scope.add_text(*args, **kwargs)

    def add_circle(self, *args, **kwargs):
        return self._root_scope.add_circle(*args, **kwargs)

    def add_segment(self, *args, **kwargs):
        return self._root_scope.add_segment(*args, **kwargs)

    def add_cubic_bezier(self, *args, **kwargs):
        return self._root_scope.add_cubic_bezier(*args, **kwargs)
