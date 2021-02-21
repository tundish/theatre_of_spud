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

import enum
import unittest

from tos.mixins.navigator import Navigator


class TestTrack(Navigator):

    topology = {str(n): [str((n + 1) % 16)] for n in range(16)}
    spots = {i: [i] for i in topology}

    Arriving = enum.Enum("Arriving", spots, type=Navigator)
    Departed = enum.Enum("Departed", spots, type=Navigator)
    Location = enum.Enum("Location", spots, type=Navigator)


class TestPatrolling(unittest.TestCase):

    def test_track(self):
        track = TestTrack()
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
