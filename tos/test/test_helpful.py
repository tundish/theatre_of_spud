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


import unittest

from tos.helpful import Helpful
from tos.types import Character
from tos.types import Directing

from turberfield.catchphrase.presenter import Presenter
from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript


class HelpfulTests(unittest.TestCase):

    def test_pause(self):
        drama = Helpful()
        fn, args, kwargs = drama.interpret(drama.match("help"))
        results = list(drama(fn, *args, **kwargs))
        drama_dialogue = list(drama.build_dialogue(*results))
        self.assertTrue(drama_dialogue)


class DirectingTests(unittest.TestCase):

    def test_quit(self):
        drama = Directing()
        drama.player = Character(names=["tester"])
        fn, args, kwargs = drama.interpret(drama.match("quit"))
        results = list(drama(fn, *args, **kwargs))
        drama_dialogue = list(drama.build_dialogue(*results))
        self.assertTrue(drama_dialogue)
