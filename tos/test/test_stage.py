#!/usr/bin/env python3
#   encoding: utf-8

# This is a parser-based, web-enabled narrative.
# Copyright (C) 2021 D. Haynes

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest

from tos.stage import Arriving
from tos.stage import Departed
from tos.stage import Location


from turberfield.dialogue.types import Stateful

class StageTests(unittest.TestCase):

    def test_enums_are_each_their_own_class(self):
        obj = Stateful()
        obj.state = Departed.car_park
        obj.state = Arriving.kitchen
        obj.state = Location.foyer
        self.assertEqual(3, len(obj._states))

    def test_enums_are_equivalent(self):
        self.assertEqual(Departed.car_park, Departed.car_park)

