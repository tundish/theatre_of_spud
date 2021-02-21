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

from tos.mixins.types import Character
from tos.mixins.patrolling import Patrolling

from tos.mixins.test.test_moving import TestTrack


class TestPatrolling(unittest.TestCase):

    def setUp(self):
        self.drama = Patrolling(TestTrack())

    def test_track(self):
        track = self.drama.nav
        self.assertTrue(all(
            a.name == b.name for a, b in zip(
                [track.Location["0"], track.Location["1"], track.Location["2"], track.Location["3"]],
                track.route(track.Location["0"], track.Location["3"])
            )
        ))
        self.assertTrue(all(
            a.name == b.name for a, b in zip(
                [track.Location["14"], track.Location["15"], track.Location["0"], track.Location["1"]],
                track.route(track.Location["14"], track.Location["1"])
            )
        ))

    def test_simple(self):
        p = Character(names=["player"])
        c = Character(names=["tester"])
        self.drama.player = p
        self.drama.add(p, c)
        self.drama.patrols = {
            c: Patrolling.Patrol(c, [self.drama.nav.Location["2"], self.drama.nav.Location["7"]], 0)
        }
        for n in range(20):
            metadata = self.drama.interlude(None, None)
            locn = c.get_state(self.drama.nav.Location)
            self.assertTrue(locn)
            with self.subTest(n=n, locn=locn):
                if n == 0:
                    self.assertEqual("2", c.get_state(self.drama.nav.Departed).name)
                    self.assertEqual("2", c.get_state(self.drama.nav.Location).name)
                    self.assertEqual("2", c.get_state(self.drama.nav.Arriving).name)
                elif n == 1:
                    self.assertEqual("2", c.get_state(self.drama.nav.Departed).name)
                    self.assertEqual("2", c.get_state(self.drama.nav.Location).name)
                    self.assertEqual("7", c.get_state(self.drama.nav.Arriving).name)
                elif n == 2:
                    self.assertEqual("2", c.get_state(self.drama.nav.Departed).name)
                    self.assertEqual("3", c.get_state(self.drama.nav.Location).name)
                    self.assertEqual("7", c.get_state(self.drama.nav.Arriving).name)
                elif n == 6:
                    self.assertEqual("7", c.get_state(self.drama.nav.Departed).name)
                    self.assertEqual("7", c.get_state(self.drama.nav.Location).name)
                    self.assertEqual("7", c.get_state(self.drama.nav.Arriving).name)
                elif n == 7:
                    self.assertEqual("7", c.get_state(self.drama.nav.Departed).name)
                    self.assertEqual("7", c.get_state(self.drama.nav.Location).name)
                    self.assertEqual("2", c.get_state(self.drama.nav.Arriving).name)
                elif n == 8:
                    self.assertEqual("7", c.get_state(self.drama.nav.Departed).name)
                    self.assertEqual("8", c.get_state(self.drama.nav.Location).name)
                    self.assertEqual("2", c.get_state(self.drama.nav.Arriving).name)
                elif n == 17:
                    self.assertEqual("7", c.get_state(self.drama.nav.Departed).name)
                    self.assertEqual("1", c.get_state(self.drama.nav.Location).name)
                    self.assertEqual("2", c.get_state(self.drama.nav.Arriving).name)
                elif n == 18:
                    self.assertEqual("2", c.get_state(self.drama.nav.Departed).name)
                    self.assertEqual("2", c.get_state(self.drama.nav.Location).name)
                    self.assertEqual("2", c.get_state(self.drama.nav.Arriving).name)
                elif n == 19:
                    self.assertEqual("2", c.get_state(self.drama.nav.Departed).name)
                    self.assertEqual("2", c.get_state(self.drama.nav.Location).name)
                    self.assertEqual("7", c.get_state(self.drama.nav.Arriving).name)
