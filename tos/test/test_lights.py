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

from tos.lights import Lights
from tos.moves import Departed
from tos.moves import Location
from tos.types import Aware
from tos.types import Character
from tos.types import Motivation


class LightsTests(unittest.TestCase):

    def setUp(self):
        self.drama = Lights()
        for obj in self.drama.build():
            self.drama.add(obj)
        self.drama.player = Character(names=["tester"]).set_state(Motivation.player, Location.car_park)
        self.drama.add(self.drama.player)

    def test_find_lights(self):
        lights = next(iter(self.drama.lookup["lights"]))
        self.assertEqual(Aware.ignorant, lights.get_state(Aware))
        self.assertEqual(Location.foyer, lights.get_state(Location))
        options = list(self.drama.match("go to the foyer"))
        fn, args, kwargs = self.drama.interpret(options)
        dlg = "\n".join(self.drama(fn, *args, **kwargs))
        metadata = self.drama.interlude(None, None)
        self.assertEqual(Location.foyer, self.drama.player.get_state(Location))
        self.assertEqual(Aware.discover, lights.get_state(Aware))
        metadata = self.drama.interlude(None, None)
        self.assertEqual(Aware.familiar, lights.get_state(Aware))

    def test_find_fuse(self):
        fuse = next(iter(self.drama.lookup["fuse"]))
        self.assertEqual(Aware.ignorant, fuse.get_state(Aware))
        self.assertEqual(Location.lighting, fuse.get_state(Location))
        options = list(self.drama.match("go to the lighting box"))
        fn, args, kwargs = self.drama.interpret(options)
        dlg = "\n".join(self.drama(fn, *args, **kwargs))
        for n in range(4):
            metadata = self.drama.interlude(None, None)
        self.assertEqual(Location.lighting, self.drama.player.get_state(Location))
        self.assertEqual(Aware.discover, fuse.get_state(Aware))

    def test_no_get_fuse(self):
        self.assertIn(self.drama.do_get, self.drama.active)
        options = list(self.drama.match("get the fuse"))
        fn, args, kwargs = self.drama.interpret(options)
        dlg = "\n".join(self.drama(fn, *args, **kwargs))
        self.assertIn("there is no fuse here", dlg.lower())

    def test_get_fuse(self):
        self.test_find_fuse()
        fuse = next(iter(self.drama.lookup["fuse"]))
        options = list(self.drama.match("get the fuse"))
        fn, args, kwargs = self.drama.interpret(options)
        dlg = "\n".join(self.drama(fn, *args, **kwargs))
        self.assertEqual(Aware.carrying, fuse.get_state(Aware))

    def test_fetch_fuse(self):
        self.test_get_fuse()
        fuse = next(iter(self.drama.lookup["fuse"]))
        options = list(self.drama.match("go to the foyer"))
        fn, args, kwargs = self.drama.interpret(options)
        dlg = "\n".join(self.drama(fn, *args, **kwargs))
        for n in range(4):
            metadata = self.drama.interlude(None, None)
        self.assertEqual(Location.foyer, self.drama.player.get_state(Location))
        self.assertEqual(Location.foyer, fuse.get_state(Location))
