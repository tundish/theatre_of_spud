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

from turberfield.dialogue.model import SceneScript

from tos.story import Story
from tos.types import Character


class StoryTests(unittest.TestCase):

    def test_progression(self):
        s = Story()
        s.drama = s.load_drama(player_name="tester")
        self.assertIsInstance(s.drama.ensemble[-1], Character)
        self.assertIsInstance(s.drama.player, Character)
