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
from tos.mixins.types import Character


class StoryTests(unittest.TestCase):

    def test_actions(self):
        s = Story()
        s.drama = s.load_drama(player_name="tester")
        self.assertTrue(s.actions)
        action = next(s.actions)
        form = "\n".join(s.render_action_form(action, autofocus=True))
        self.assertIn('<label for="input-cmd-text" id="input-cmd-text-tip">&gt;</label>', form)
        self.assertIn("<fieldset>", form)
        self.assertIn("</fieldset>", form)
        self.assertIn('autofocus="autofocus"', form)
        self.assertIn('placeholder="?"', form)
        self.assertIn('pattern="[\\w ]{1,36}"', form)  # Don't forget the space
        self.assertIn('<button type="submit">Enter</button>', form, form)

    def test_progression(self):
        s = Story()
        s.drama = s.load_drama(player_name="tester")
        self.assertIsInstance(s.drama.player, Character)
        self.assertIsInstance(s.drama, Story.Act1)
