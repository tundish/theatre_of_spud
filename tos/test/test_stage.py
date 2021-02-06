#!/usr/bin/env python3
#   encoding: utf-8

# This is a parser-based, web-enabled narrative.
# Copyright (C) 2021 D E Haynes

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

import pickle
import unittest

from tos.stage import Arriving
from tos.stage import Character
from tos.stage import Departed
from tos.stage import Location
from tos.stage import Stage

from turberfield.dialogue.types import Stateful
from turberfield.utils.assembly import Assembly


class NavigatorTests(unittest.TestCase):

    def test_enums_are_each_their_own_class(self):
        obj = Stateful()
        obj.state = Departed.car_park
        obj.state = Arriving.kitchen
        obj.state = Location.foyer
        self.assertEqual(3, len(obj._states))

    def test_enums_are_equivalent_but_not_equal(self):
        self.assertNotEqual(Arriving.car_park, Departed.car_park)
        self.assertEqual(Arriving.car_park.name, Departed.car_park.name)
        self.assertEqual(Arriving.car_park.value, Departed.car_park.value)

    def test_enums_are_picklable(self):
        rv = pickle.dumps(Arriving.car_park)
        self.assertEqual(Arriving.car_park, pickle.loads(rv))

    def test_enums_can_be_assembled(self):
        self.assertTrue(Assembly.register(Arriving))
        rv = Assembly.dumps(Arriving.car_park)
        self.assertEqual(Arriving.car_park, Assembly.loads(rv), rv)


class StoryTests(unittest.TestCase):

    def setUp(self):
        self.ensemble = [
            Character(names=["player"])
        ]

    def test_movement(self):
        drama = Stage()
