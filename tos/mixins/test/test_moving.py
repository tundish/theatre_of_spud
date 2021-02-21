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

import pickle
import sys
import unittest

from tos.map import Map
from tos.mixins.moving import Moving
from tos.mixins.types import Character
from tos.mixins.types import Mode
from tos.mixins.types import Proximity

from turberfield.dialogue.types import Stateful
from turberfield.utils.assembly import Assembly


class NavigatorTests(unittest.TestCase):

    def test_enums_are_each_their_own_class(self):
        obj = Stateful()
        obj.state = Map.Departed.car_park
        obj.state = Map.Arriving.kitchen
        obj.state = Map.Location.foyer
        self.assertEqual(3, len(obj._states))

    def test_enums_are_equivalent_but_not_equal(self):
        self.assertNotEqual(Map.Arriving.car_park, Map.Departed.car_park)
        self.assertEqual(Map.Arriving.car_park.name, Map.Departed.car_park.name)
        self.assertEqual(Map.Arriving.car_park.value, Map.Departed.car_park.value)

    def test_enums_are_picklable(self):
        rv = pickle.dumps(Map.Arriving.car_park)
        self.assertEqual(Map.Arriving.car_park, pickle.loads(rv))

    def test_enums_can_be_assembled(self):
        self.assertTrue(Assembly.register(Map.Arriving))
        rv = Assembly.dumps(Map.Arriving.car_park)
        self.assertEqual(Map.Arriving.car_park, Assembly.loads(rv), rv)

    def test_navigation(self):
        m = Map()
        for locn in Map.Location:
            for dest in Map.Arriving:
                with self.subTest(locn=locn, dest=dest):
                    route = m.route(locn, dest)
                    if locn.name == dest.name:
                        self.assertEqual((locn,), route)
                    else:
                        self.assertTrue(route)
                        #print(locn.name, dest.name, len(route), route, file=sys.stderr)
        #print(*Location.routes, file=sys.stderr)


class MovingTests(unittest.TestCase):

    def setUp(self):
        nav = Map()
        self.drama = Moving(nav)

    def test_movement(self):
        self.drama.player = Character(names=["player"]).set_state(
            Mode.playing, self.drama.nav.Location.car_park
        )
        self.drama.add(self.drama.player)
        self.assertIn(self.drama.do_go, self.drama.active)
        options = list(self.drama.match("go backstage"))
        self.assertTrue(options, options)
        fn, args, kwargs = self.drama.interpret(options)
        self.assertTrue(fn)
        dlg = "\n".join(self.drama(fn, *args, **kwargs))
        self.assertEqual(Map.Location.car_park, self.drama.player.get_state(Map.Location))
        self.assertEqual(Map.Departed.car_park, self.drama.player.get_state(Map.Departed))
        self.assertEqual(Map.Arriving.backstage, self.drama.player.get_state(Map.Arriving))

    def test_proximity(self):
        other = Character(names=["other"]).set_state(Map.Location.backstage)
        self.drama.player = Character(names=["player"]).set_state(Mode.playing, Map.Location.car_park)
        self.drama.add(self.drama.player, other)
        self.assertFalse(other.get_state(Proximity))
        metadata = self.drama.interlude(None, None)
        self.assertEqual(Proximity.distant, other.get_state(Proximity))

        options = list(self.drama.match("go backstage"))
        fn, args, kwargs = self.drama.interpret(options)
        dlg = "\n".join(self.drama(fn, *args, **kwargs))
        for n in range(4):
            metadata = self.drama.interlude(None, None)
            with self.subTest(n=n, locn=self.drama.player.get_state(Map.Location)):
                if n == 2:
                    self.assertEqual(Map.Location.wings, self.drama.player.get_state(Map.Location))
                    self.assertEqual(Proximity.outside, other.get_state(Proximity))
                elif n == 3:
                    self.assertEqual(Map.Location.backstage, self.drama.player.get_state(Map.Location))
                    self.assertEqual(Proximity.present, other.get_state(Proximity))
                else:
                    self.assertEqual(Proximity.distant, other.get_state(Proximity))

