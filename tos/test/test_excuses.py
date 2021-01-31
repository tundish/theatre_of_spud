#!/usr/bin/env python3
# encoding: utf-8

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

from collections import namedtuple
import enum
import random
from turberfield.catchphrase.drama import Drama



class Motivation(enum.Enum):

    acting = enum.auto()
    paused = enum.auto()
    player = enum.auto()
    herald = enum.auto()


class SickNote:

    Message = namedtuple("SickNote", ["parent", "child", "excuse", "tags"])

    @staticmethod
    def statement(msg):
        pass

    @staticmethod
    def report(msg, n=None):
        aux = ["is going to", "has to"]
        return "{parent[0]} says {parent[1]} {0} {1}".format(
            random.choice(aux) if n is None else aux[n],
            msg.excuse.format(**msg._asdict()), **msg._asdict()
        )


class Tuition(Drama):
    pass


class SickNotesTests(unittest.TestCase):

    def test_excuses(self):
        note = SickNote.Message(
            ("Angela", "she"), ("Bobby", "he"),
            "take {child[0]} to the {tags[0]} in {tags[1]}", ["caravan", "Minehead"]
        )
        rv = "Angela says she has to take Bobby to the caravan in Minehead"
        self.assertEqual(rv, SickNote.report(note, n=1))


class TuitionTests(unittest.TestCase):

    def test_initial(self):
        drama = Tuition()
        self.assertTrue(drama.active)
        self.assertTrue("help" in "".join([i.__doc__ for i in drama.active]))
        self.assertTrue("look" in "".join([i.__doc__ for i in drama.active]))
