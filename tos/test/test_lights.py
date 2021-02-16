#!/usr/bin/env python3
# encoding: utf-8

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

import unittest


#

from tos.moves import Location
from tos.moves import Moves
from tos.types import Aware
from tos.types import Artifact
from tos.types import Character
from tos.types import Motivation


class Lights(Moves):

    def build(self):
        yield from super().build()
        yield Artifact(names=["lights"]).set_state(Aware.ignorant, Location.foyer)
        yield Artifact(names=["fuse"]).set_state(Aware.ignorant, Location.lighting)


class LightsTests(unittest.TestCase):

    def setUp(self):
        self.drama = Lights()
        for obj in self.drama.build():
            self.drama.add(obj)
        self.drama.player = Character(names=["tester"]).set_state(Motivation.player, Location.car_park)
        self.drama.add(self.drama.player)

    def test_find_fuse(self):
        lights = next(iter(self.drama.lookup["lights"]))
        options = list(self.drama.match("go to the foyer"))
        self.assertTrue(options, options)
        fn, args, kwargs = self.drama.interpret(options)
        dlg = "\n".join(self.drama(fn, *args, **kwargs))
        metadata = self.drama.interlude(None, None)
        self.assertEqual(Location.foyer, self.drama.player.get_state(Location))
