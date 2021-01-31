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


class Knowledge:

    Noun = namedtuple("Noun", ["name", "gender"])
    Message = namedtuple(
        "Message", ["attribution", "nouns", "intends", "implies", "tags"]
    )

    @staticmethod
    def implications(msg):
        yield from (i.format(**msg._asdict()) for i in msg.implies)

    @staticmethod
    def intentions(msg):
        yield from (i.format(**msg._asdict()) for i in msg.intends)

    @staticmethod
    def report(msg, n=None):
        attr = msg.attribution
        lookup = {"f": "she", "m": "he", "n": "their"}.get(attr.gender, "it")
        msg = msg._replace(attribution=attr._replace(name=lookup))
        for i in Knowledge.intentions(msg):
            yield f"{attr.name} says {i}"


class Tuition(Drama):
    pass


class SickNotesTests(unittest.TestCase):

    def test_excuses(self):
        note = Knowledge.Message(
            Knowledge.Noun("Angela", "f"), (Knowledge.Noun("Bobby", "m"),),
            ("{attribution.name} is taking {nouns[0].name} to the {tags[0]} in {tags[1]}",
             "{attribution.name} has to take {nouns[0].name} to the {tags[0]} in {tags[1]}"),
            ("{attribution.name} is at the {tags[0]}", "{attribution.name} is in {tags[1]}",
             "{nouns[0].name} is at the {tags[0]}", "{nouns[0].name} is in {tags[1]}"),
            ("caravan", "Minehead")
        )
        report = "Angela says she has to take Bobby to the caravan in Minehead"
        self.assertEqual(report, list(Knowledge.report(note))[1])
        fact = "Bobby is in Minehead"
        self.assertEqual(rv, list(Knowledge.implications(note))[1])


class TuitionTests(unittest.TestCase):

    def test_initial(self):
        drama = Tuition()
        self.assertTrue(drama.active)
        self.assertTrue("help" in "".join([i.__doc__ for i in drama.active]))
        self.assertTrue("look" in "".join([i.__doc__ for i in drama.active]))
