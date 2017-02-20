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

from lxml import etree

from Valentina.Geometry.Vector2D import Vector2D
from Valentina.Pattern.Measurement import Measurements, Measurement
from Valentina.Pattern.Pattern import Pattern
from Valentina.Xml.Objectivity import (IntAttribute, FloatAttribute, StringAttribute,
                                       XmlObjectAdaptator)
from Valentina.Xml.XmlFile import XmlFileMixin
from .Measurements import VitFile

import Valentina.Pattern.Calculation as Calculation

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class CalculationMixin:

    __attributes__ = (
        IntAttribute('id'),
    )

    ##############################################

    def to_calculation(self, pattern):

        raise NotImplementedError

####################################################################################################

class LinePropertiesMixin:

    __attributes__ = (
        StringAttribute('line_color', 'lineColor'),
        StringAttribute('line_style', 'typeLine'),
    )

    __COLORS__ = (
        'black',
        'blue',
        'cornflowerblue',
        'darkBlue',
        'darkGreen',
        'darkRed',
        'darkviolet',
        'deeppink',
        'deepskyblue',
        'goldenrod',
        'green',
        'lightsalmon',
        'lime',
        'mediumseagreen',
        'orange',
        'violet',
        'yellow',
    )

    __LINE_STYLE__ = (
        'dashDotDotLine',
        'dashDotLine',
        'dashLine',
        'dotLine',
        'hair', # should be solid
        'none',
    )

####################################################################################################

# angle
# angle1
# angle2
# arc
# axisP1
# axisP2
# axisType
# baseLineP1
# baseLineP2
# basePoint
# c1Center
# c1Radius
# c2Center
# c2Radius
# cCenter
# center
# color
# cRadius
# crossPoint
# curve
# curve1
# curve2
# dartP1
# dartP2
# dartP3
# duplicate
# firstArc
# firstPoint
# hCrossPoint
# id
# idObject
# length
# length1
# length2
# lineColor
# mx
# mx1
# mx2
# my
# my1
# my2
# name
# name1
# name2
# object (group)
# p1Line
# p1Line1
# p1Line2
# p2Line
# p2Line1
# p2Line2
# point1
# point2
# point3
# point4
# pShoulder
# pSpline
# radius
# radius1
# radius2
# rotationAngle
# secondArc
# secondPoint
# spline
# splinePath
# suffix
# tangent
# thirdPoint
# tool
# type
# typeLine
# vCrossPoint
# visible (group)
# x
# y

class XyMixin:
    __attributes__ = (
        StringAttribute('x'),
        StringAttribute('y'),
    )

class FirstSecondPointMixin:
    __attributes__ = (
        IntAttribute('first_point', 'firstPoint'),
        IntAttribute('second_point', 'secondPoint'),
    )

class FirstSecondThirdPointMixin(FirstSecondPointMixin):
    __attributes__ = (
        IntAttribute('third_point', 'thirdPoint'),
    )

class BasePointMixin:
    __attributes__ = (
        IntAttribute('base_point', 'basePoint'),
    )

class Line1Mixin:
    __attributes__ = (
        IntAttribute('point1_line1', 'p1Line1'),
        IntAttribute('point2_line1', 'p2Line1'),
    )

class Line2Mixin:
    __attributes__ = (
        IntAttribute('point1_line2', 'p1Line2'),
        IntAttribute('point2_line2', 'p2Line2'),
    )

class Line12Mixin(Line1Mixin, Line2Mixin):
    pass

class LengthMixin:
    __attributes__ = (
        StringAttribute('length'),
    )

class AngleMixin:
    __attributes__ = (
        StringAttribute('angle'),
    )

class LengthAngleMixin(LengthMixin, AngleMixin):
    pass

####################################################################################################

class PointMixin(CalculationMixin):

    __tag__ = 'point'
    __attributes__ = (
        StringAttribute('name'),
        FloatAttribute('mx'),
        FloatAttribute('my'),
    )

    __calculation__ = None

    ##############################################

    def to_calculation(self, pattern):

        kwargs = self.to_dict(exclude=('mx', 'my')) # id'
        kwargs['label_offset'] = Vector2D(self.mx, self.my)
        return self.__calculation__(pattern, **kwargs)

####################################################################################################

class PointLinePropertiesMixin(PointMixin, LinePropertiesMixin):
    pass

####################################################################################################

class AlongLinePoint(XmlObjectAdaptator, PointLinePropertiesMixin, FirstSecondPointMixin, LengthMixin):

    # <point id="27" firstPoint="25" typeLine="none" mx="0.1" secondPoint="26"
    # length="-Line_Bt_Ct" name="Dt" lineColor="black" type="alongLine" my="0.2"/>

    __type__ = 'alongLine'
    __calculation__ = Calculation.AlongLinePoint

####################################################################################################

class BissectorPoint(XmlObjectAdaptator, PointLinePropertiesMixin, FirstSecondThirdPointMixin, LengthMixin):

    # <point id="13" firstPoint="2" thirdPoint="5" typeLine="hair" mx="0.1" secondPoint="1"
    # length="Line_A_X" name="B" lineColor="deepskyblue" type="bisector" my="0.2"/>

    __type__ = 'bisector'
    # __calculation__ = Calculation.BissectorPoint

####################################################################################################

# __type__ = 'curveIntersectAxis'
# <point id="68" basePoint="64" typeLine="hair" mx="0.5" name="Cax1" lineColor="blue"
# type="curveIntersectAxis" angle="10" curve="59" my="-3.1"/>

# __type__ = 'cutArc'
# <point id="73" mx="-3.7" length="30" arc="72" name="Cl3" type="cutArc" my="1.4"/>

# __type__ = 'cutSpline'
# <point id="54" spline="53" mx="0.1" length="10" name="Cl1" type="cutSpline" my="0.2"/>

# __type__ = 'cutSplinePath'
# <point id="60" mx="0.1" splinePath="59" length="20" name="CI2" type="cutSplinePath" my="0.2"/>

####################################################################################################

class EndLinePoint(XmlObjectAdaptator, PointLinePropertiesMixin, BasePointMixin, LengthAngleMixin):

    # <point id="2" basePoint="1" typeLine="hair" mx="0.1" length="10" name="X"
    # lineColor="blue" type="endLine" angle="360" my="0.25"/>

    __type__ = 'endLine'
    __calculation__ = Calculation.EndLinePoint

####################################################################################################

class HeightPoint(XmlObjectAdaptator, PointLinePropertiesMixin, BasePointMixin, Line1Mixin):

    # <point id="18" basePoint="7" typeLine="hair" mx="0.1" p2Line="14" name="P" p1Line="2"
    # lineColor="mediumseagreen" type="height" my="0.2"/>

    __type__ = 'height'
    # __calculation__ = Calculation.HeightPoint

####################################################################################################

class LineIntersectPoint(XmlObjectAdaptator, PointMixin, Line12Mixin):

    # <point id="17" mx="0.1" p1Line2="2" p1Line1="1" name="I" type="lineIntersect" my="0.2"
    # p2Line1="12" p2Line2="14"/>

    __type__ = 'lineIntersect'
    __calculation__ = Calculation.LineIntersectPoint

####################################################################################################

class LineIntersectAxisPoint(XmlObjectAdaptator, PointLinePropertiesMixin, BasePointMixin, Line1Mixin, AngleMixin):

    # <point id="20" basePoint="14" typeLine="hair" mx="0.4" p2Line="1" name="AxAn" p1Line="5"
    # lineColor="goldenrod" type="lineIntersectAxis" angle="150" my="-1.8"/>

    __type__ = 'lineIntersectAxis'
    # __calculation__ = Calculation.LineIntersectAxisPoint

####################################################################################################

class NormalPoint(XmlObjectAdaptator, PointLinePropertiesMixin, FirstSecondPointMixin, LengthAngleMixin):

    # <point id="26" firstPoint="25" typeLine="hair" mx="0.1" secondPoint="24" length="5"
    # name="Ct" lineColor="blue" type="normal" angle="0" my="0.1"/>

    __type__ = 'normal'
    __calculation__ = Calculation.NormalPoint

####################################################################################################

# __type__ = 'pointFromArcAndTangent'
# <point id="84" tangent="83" mx="-1.3" crossPoint="1" arc="77" name="Ctan" type="pointFromArcAndTangent" my="1.7"/>

# __type__ = 'pointFromCircleAndTangent'
# <point id="81" tangent="80" mx="-2.9" cRadius="3" cCenter="71" crossPoint="1" name="Cp1" type="pointFromCircleAndTangent" my="-2.7"/>

# __type__ = 'pointOfContact'
# <point id="19" radius="Line_A_M*3/2" center="4" firstPoint="1" mx="0.1" secondPoint="5" name="R" type="pointOfContact" my="0.2"/>

####################################################################################################

class PointOfIntersection(XmlObjectAdaptator, PointMixin, FirstSecondPointMixin):

    # <point id="14" firstPoint="2" mx="0.1" secondPoint="5" name="XY" type="pointOfIntersection" my="0.2"/>

    __type__ = 'pointOfIntersection'
    __calculation__ = Calculation.PointOfIntersection

####################################################################################################

# __type__ = 'pointOfIntersectionArcs'
# <point id="78" firstArc="72" mx="-1.3" secondArc="77" crossPoint="1" name="Ci2" type="pointOfIntersectionArcs" my="2."/>

# __type__ = 'pointOfIntersectionCircles'
# <point id="79" c1Center="71" mx="0.1" crossPoint="1" c1Radius="15" name="Ci3" c2Radius="18"
# type="pointOfIntersectionCircles" my="0.2" c2Center="76"/>

# __type__ = 'pointOfIntersectionCurves'
# <point id="67" mx="0.9" curve1="59" vCrossPoint="1" curve2="66" hCrossPoint="1" name="Ci1"
# type="pointOfIntersectionCurves" my="-3.8"/>

####################################################################################################

class ShoulderPoint(XmlObjectAdaptator, PointLinePropertiesMixin, Line1Mixin, LengthMixin):

    # <point id="21" typeLine="hair" mx="0.7" p2Line="14" length="Line_X_XY*2" pShoulder="20" name="Sh"
    # p1Line="5" lineColor="lightsalmon" type="shoulder" my="-1.3"/>

    __type__ = 'shoulder'
    # __calculation__ = Calculation.ShoulderPoint
    __attributes__ = (
        IntAttribute('shoulder_point', 'pShoulder'),
    )

####################################################################################################

class SinglePoint(XmlObjectAdaptator, PointMixin, XyMixin):

    # <point id="1" mx="0.1" x="0.79375" y="1.05833" name="A" type="single" my="0.2"/>

    __type__ = 'single'
    __calculation__ = Calculation.SinglePoint

####################################################################################################

# __type__ = 'triangle'
# <point id="28" axisP2="25" axisP1="24" firstPoint="27" mx="0.8" secondPoint="26" name="T1"
# type="triangle" my="1.4"/>

# __type__ = 'trueDarts'
# <point id="44" mx2="-3.9" baseLineP2="39" baseLineP1="38" mx1="0.2" dartP3="42" name1="Td1"
# dartP2="41" point2="46" point1="45" name2="Td2" my2="-0.1" type="trueDarts" my1="-2.5"
# dartP1="43"/>

####################################################################################################

class Point:

    # We cannot use a metaclass to auto-register due to XmlObjectAdaptator (right ?)
    __TYPES__ = {
        'alongLine': AlongLinePoint,
        'bisector': None,
        'curveIntersectAxis': None,
        'cutArc': None,
        'cutSpline': None,
        'cutSplinePath': None,
        'endLine': EndLinePoint,
        'height': None,
        'lineIntersect': LineIntersectPoint,
        'lineIntersectAxis': None,
        'normal': NormalPoint,
        'pointFromArcAndTangent': None,
        'pointFromCircleAndTangent': None,
        'pointOfContact': None,
        'pointOfIntersection': PointOfIntersection,
        'pointOfIntersectionArcs': None,
        'pointOfIntersectionCircles': None,
        'pointOfIntersectionCurves': None,
        'shoulder': None,
        'single': SinglePoint,
        'triangle': None,
        'trueDarts': None,
    }

####################################################################################################

class Line(XmlObjectAdaptator, CalculationMixin, LinePropertiesMixin, FirstSecondPointMixin):

    # <line id="47" firstPoint="38" typeLine="hair" secondPoint="45" lineColor="blue"/>

    __tag__ = 'line'

    ##############################################

    def to_calculation(self, pattern):

        return Calculation.Line(pattern, **self.to_dict()) # exclude=('id')

####################################################################################################

class SplineMixin(CalculationMixin):
    __tag__ = 'spline'

####################################################################################################

class SimpleInteractiveSpline(XmlObjectAdaptator, SplineMixin):

    # <spline id="53" angle2="138.403" length2="14.0301" angle1="329.987" length1="18.2062"
    # point4="52" type="simpleInteractive" point1="51" color="blue"/>

    __type__ = 'simpleInteractive'
    __attributes__ = (
        IntAttribute('first_point', 'point1'),
        IntAttribute('second_point', 'point4'),
        StringAttribute('length1'),
        StringAttribute('length2'),
        StringAttribute('angle1'),
        StringAttribute('angle2'),
        StringAttribute('line_color', 'color'),
    )

    ##############################################

    def to_calculation(self, pattern):

        return Calculation.SimpleInteractiveSpline(pattern, **self.to_dict()) # exclude=('id')

####################################################################################################

# <spline id="57" duplicate="1" point4="52" point2="55" point3="56" type="cubicBezier" point1="51" color="goldenrod"/>

# <spline id="66" type="cubicBezierPath" color="deepskyblue">
#     <pathPoint pSpline="51"/>
#     <pathPoint pSpline="52"/>
#     <pathPoint pSpline="58"/>
#     <pathPoint pSpline="61"/>
#     <pathPoint pSpline="63"/>
#     <pathPoint pSpline="64"/>
#     <pathPoint pSpline="65"/>
# </spline>

# <spline id="59" type="pathInteractive" color="violet">
#     <pathPoint angle2="333.352" length2="25.9685" length1="0" angle1="153.352" pSpline="51"/>
#     <pathPoint angle2="82.712" length2="15.9887" length1="9.36267" angle1="262.712" pSpline="52"/>
#     <pathPoint angle2="254.923" length2="1.78344" length1="7.70133" angle1="74.9232" pSpline="58"/>
# </spline>

####################################################################################################

class Spline:

    # We cannot use a metaclass to auto-register due to XmlObjectAdaptator (right ?)
    __TYPES__ = {
        'cubicBezier': None,
        'cubicBezierPath': None,
        'pathInteractive': None,
        'simpleInteractive': SimpleInteractiveSpline,
    }

####################################################################################################

# <arc id="86" radius="10" center="83" angle1="45" length="30" type="arcWithLength" color="black"/>
# <arc id="72" radius="10" angle2="-30" center="71" angle1="30" type="simple" color="black"/>
# __ARC_TYPE__ = (
#     'arcWithLength',
#     'simple',
#     )

# <elArc id="87" angle2="300" center="83" radius2="15" rotationAngle="60" radius1="10" angle1="30" type="simple" color="lime"/>
# __ELLIPSE_TYPE__ = (
#     'simple',
#     )

# <operation id="110" center="89" suffix="mir2" axisType="1" type="flippingByAxis">
#     <source>
#         <item idObject="88"/>
#     </source>
#     <destination>
#         <item idObject="111" mx="0.132292" my="0.264583"/>
#     </destination>
# </operation>

# <operation id="108" suffix="mir" p2Line="89" p1Line="88" type="flippingByLine">
#     <source>
#         <item idObject="90"/>
#     </source>
#     <destination>
#         <item idObject="109" mx="0.132292" my="0.264583"/>
#     </destination>
# </operation>

# <operation id="113" suffix="mov" length="15" type="moving" angle="160">
#     <source>
#         <item idObject="88"/>
#     </source>
#     <destination>
#         <item idObject="114" mx="-1.4973" my="1.56825"/>
#     </destination>
# </operation>

# <operation id="101" center="94" suffix="rot" type="rotation" angle="30">
#     <source>
#         <item idObject="88"/>
#     </source>
#     <destination>
#         <item idObject="102" mx="-0.193626" my="0.738642"/>
#     </destination>
# </operation>

# __OPERATION_TYPE__ = (
#     'flippingByAxis',
#     'flippingByLine',
#     'moving',
#     'rotation',
# )

####################################################################################################

class CalculationDispatcher:

    _logger = _module_logger.getChild('CalculationDispatcher')

    __TAGS__ = {
        'arc': None,
        'ellipse': None,
        'line': Line,
        'operation': None,
        'point': Point,
        'spline': Spline,
        }

    ##############################################

    @staticmethod
    def from_xml(element):

        tag_class = CalculationDispatcher.__TAGS__[element.tag]
        if hasattr(tag_class, '__TYPES__'):
            cls = tag_class.__TYPES__[element.attrib['type']]
        else:
            cls = tag_class
        if cls is not None:
            return cls(element)
        else:
            raise NotImplementedError

####################################################################################################

class ValFile(XmlFileMixin):

    _logger = _module_logger.getChild('ValFile')

    ##############################################

    def __init__(self, path):

        XmlFileMixin.__init__(self, path)
        self._vit_file = None
        self._pattern = None
        self._read()

    ##############################################

    @property
    def measurements(self):
        return self._vit_file.measurements

    @property
    def pattern(self):
        return self._pattern

    ##############################################

    def _read(self):

        # <?xml version='1.0' encoding='UTF-8'?>
        # <pattern>
        #     <!--Pattern created with Valentina (http://www.valentina-project.org/).-->
        #     <version>0.4.0</version>
        #     <unit>cm</unit>
        #     <author/>
        #     <description/>
        #     <notes/>
        #     <measurements/>
        #     <increments/>
        #     <draw name="Pattern piece 1">
        #         <calculation/>
        #         <modeling/>
        #         <details/>
        #         <groups/>
        #     </draw>
        # </pattern>

        tree = self._parse()

        measurements_path = self._get_xpath_element(tree, 'measurements').text
        self._vit_file = VitFile(measurements_path)

        pattern = Pattern(self._vit_file.measurements)
        self._pattern = pattern

        elements = self._get_xpath_element(tree, 'draw/calculation')
        for element in elements:
            try:
                xml_calculation = CalculationDispatcher.from_xml(element)
                calculation = xml_calculation.to_calculation(pattern)
                pattern.add(calculation)
            except NotImplementedError:
                self._logger.warning('Not implemented calculation\n' +  str(etree.tostring(element)))

        pattern.eval()
