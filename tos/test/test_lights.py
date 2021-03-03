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
from tos.lights import Switch
from tos.map import Map
from tos.mixins.types import Awareness
from tos.mixins.types import Character
from tos.mixins.types import Mode


class LightsTests(unittest.TestCase):

    def setUp(self):
        self.drama = Lights(Map())
        for obj in self.drama.build():
            self.drama.add(obj)
        self.drama.player = Character(names=["tester"]).set_state(Mode.playing, Map.Location.car_park)
        next(iter(self.drama.lookup["fuse"])).state = Awareness.indicate
        next(iter(self.drama.lookup["lights"])).state = Awareness.indicate
        self.drama.active.add(self.drama.do_lights_off)
        self.drama.active.add(self.drama.do_lights_on)

    def test_find_lights(self):
        lights = next(iter(self.drama.lookup["lights"]))
        self.assertEqual(Awareness.indicate, lights.get_state(Awareness))
        self.assertEqual(Map.Location.foyer, lights.get_state(Map.Location))
        options = list(self.drama.match("go to the foyer"))
        fn, args, kwargs = self.drama.interpret(options)
        dlg = "\n".join(self.drama(fn, *args, **kwargs))
        metadata = self.drama.interlude(None, None)
        self.assertEqual(Map.Location.foyer, self.drama.player.get_state(Map.Location))
        self.assertEqual(Awareness.discover, lights.get_state(Awareness))
        metadata = self.drama.interlude(None, None)
        self.assertEqual(Awareness.familiar, lights.get_state(Awareness))

    def test_find_fuse(self):
        fuse = next(iter(self.drama.lookup["fuse"]))
        self.assertEqual(Awareness.indicate, fuse.get_state(Awareness))
        self.assertEqual(Map.Location.lighting, fuse.get_state(Map.Location))
        options = list(self.drama.match("go to the lighting box"))
        fn, args, kwargs = self.drama.interpret(options)
        dlg = "\n".join(self.drama(fn, *args, **kwargs))
        for n in range(4):
            metadata = self.drama.interlude(None, None)
        self.assertEqual(Map.Location.lighting, self.drama.player.get_state(Map.Location))
        self.assertEqual(Awareness.discover, fuse.get_state(Awareness))

    def test_no_get_fuse(self):
        self.assertIn(self.drama.do_get, self.drama.active)
        options = list(self.drama.match("get the fuse"))
        fn, args, kwargs = self.drama.interpret(options)
        dlg = "\n".join(self.drama(fn, *args, **kwargs))
        self.assertIn("there is no fuse here", dlg.lower())

    def test_no_fit_fuse(self):
        self.assertIn(self.drama.do_get, self.drama.active)
        options = list(self.drama.match("fit the fuse"))
        fn, args, kwargs = self.drama.interpret(options)
        self.assertFalse(fn)

    def test_no_light_off(self):
        self.assertIn(self.drama.do_lights_off, self.drama.active)
        for cmd in (
            "switch off lights", "turn off lights",
            "switch lights off", "turn lights off",
        ):
            with self.subTest(cmd=cmd):
                options = list(self.drama.match(cmd))
                fn, args, kwargs = self.drama.interpret(options)
                self.assertTrue(fn)
                dlg = "\n".join(self.drama(fn, *args, **kwargs))
                self.assertFalse(dlg)

    def test_no_light_on(self):
        self.assertIn(self.drama.do_lights_on, self.drama.active)
        for cmd in (
            "switch on lights", "turn on lights",
            "switch lights on", "turn lights on",
        ):
            with self.subTest(cmd=cmd):
                options = list(self.drama.match(cmd))
                fn, args, kwargs = self.drama.interpret(options)
                self.assertTrue(fn)
                dlg = "\n".join(self.drama(fn, *args, **kwargs))
                self.assertFalse(dlg)

    def test_get_fuse(self):
        self.test_find_fuse()
        self.assertEqual(Map.Location.lighting, self.drama.player.get_state(Map.Location))
        self.assertIn(self.drama.do_get, self.drama.active)
        fuse = next(iter(self.drama.lookup["fuse"]))
        options = list(self.drama.match("get the fuse"))
        fn, args, kwargs = self.drama.interpret(options)
        dlg = "\n".join(self.drama(fn, *args, **kwargs))
        self.assertEqual(Awareness.carrying, fuse.get_state(Awareness))

    def test_fetch_fuse(self):
        self.test_get_fuse()
        fuse = next(iter(self.drama.lookup["fuse"]))
        options = list(self.drama.match("go to the foyer"))
        fn, args, kwargs = self.drama.interpret(options)
        dlg = "\n".join(self.drama(fn, *args, **kwargs))
        for n in range(4):
            metadata = self.drama.interlude(None, None)
        self.assertEqual(Map.Location.foyer, self.drama.player.get_state(Map.Location))
        self.assertEqual(Map.Location.foyer, fuse.get_state(Map.Location))

    def test_fit_fuse(self):
        self.test_fetch_fuse()
        lights = next(iter(self.drama.lookup["lights"]))
        fuse = next(iter(self.drama.lookup["fuse"]))
        self.assertEqual(Switch.broken, lights.get_state(Switch))
        options = list(self.drama.match("fit the fuse"))
        fn, args, kwargs = self.drama.interpret(options)
        dlg = "\n".join(self.drama(fn, *args, **kwargs))
        self.assertEqual(Awareness.complete, fuse.get_state(Awareness))
        self.assertEqual(Map.Location.foyer, fuse.get_state(Map.Location))
        self.assertNotEqual(Switch.broken, lights.get_state(Switch))

    def test_light_off(self):
        self.test_fit_fuse()
        lights = next(iter(self.drama.lookup["lights"]))
        for cmd in (
            "switch off lights", "turn off lights",
            "switch lights off", "turn lights off",
        ):
            with self.subTest(cmd=cmd):
                options = list(self.drama.match(cmd))
                fn, args, kwargs = self.drama.interpret(options)
                self.assertTrue(fn)
                dlg = "\n".join(self.drama(fn, *args, **kwargs))
                self.assertIn("out", dlg)
                self.assertEqual(Switch.opened, lights.get_state(Switch))

    def test_light_on(self):
        self.test_fit_fuse()
        lights = next(iter(self.drama.lookup["lights"]))
        for cmd in (
            "switch on lights", "turn on lights",
            "switch lights on", "turn lights on",
        ):
            with self.subTest(cmd=cmd):
                options = list(self.drama.match(cmd))
                fn, args, kwargs = self.drama.interpret(options)
                self.assertTrue(fn)
                dlg = "\n".join(self.drama(fn, *args, **kwargs))
                self.assertIn("on", dlg)
                self.assertEqual(Switch.closed, lights.get_state(Switch))

