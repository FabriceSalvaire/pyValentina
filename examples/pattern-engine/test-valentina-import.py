####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2018 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

from pathlib import Path

from Patro.Common.Logging import Logging
Logging.setup_logging()

from Patro.FileFormat.Valentina.Pattern import ValFileReader
from PatroExample import find_data_path

####################################################################################################

# val_file = 'several-pieces.val'
val_file = 'flat-city-trouser.val'
val_path = find_data_path('patterns-valentina', val_file)

val_file = ValFileReader(val_path)
pattern = val_file.pattern

####################################################################################################

# pattern.dump()

# for calculation in pattern.calculations:
#     print(calculation.to_python())

# nodes = pattern.calculator.dag.topological_sort()
# for node in nodes:
#     print(node.data)

# output = Path('output')
# output.mkdir(exist_ok=True)

# val_file.write(output.joinpath('write-test.val'))
