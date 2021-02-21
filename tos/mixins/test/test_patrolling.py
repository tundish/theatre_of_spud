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

from collections import namedtuple
import enum
import unittest

from tos.mixins.moving import Moving
from tos.mixins.navigator import Navigator
from tos.mixins.types import Character
from tos.mixins.types import Mode


class Patrolling(Moving):

    Patrol = namedtuple("Patrol", ["npc", "orders", "pos"])

    def __init__(self, *args, patrols=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.patrols = {i.npc: i for i in patrols or []}

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        for c, p in self.patrols.items():
            if c.get_state(Mode) == Mode.pausing:
                continue

            pos = p.pos or 0
            hop = p.orders[pos]
            locn = c.get_state(self.nav.Location)
            c.state = locn or self.nav.Location[hop.name]

            dst = c.get_state(self.nav.Arriving)
            if not dst or dst.name != hop.name:
                c.state = self.nav.Arriving[hop.name]

            locn = c.get_state(self.nav.Location)
            if locn.name == c.get_state(self.nav.Arriving).name:
                c.state = self.nav.Departed[locn.name]
                self.patrols[c] = p._replace(pos=(pos + 1) % len(p.orders))
        return rv


class TestTrack(Navigator):

    topology = {str(n): [str((n + 1) % 16)] for n in range(16)}
    spots = {i: [i] for i in topology}

    Arriving = enum.Enum("Arriving", spots, type=Navigator)
    Departed = enum.Enum("Departed", spots, type=Navigator)
    Location = enum.Enum("Location", spots, type=Navigator)


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
