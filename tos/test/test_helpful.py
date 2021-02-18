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


import importlib.resources
import unittest

from tos.helpful import Helpful

from turberfield.catchphrase.presenter import Presenter
from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript



class DialogueTests(unittest.TestCase):

    def setUp(self):
        pkg = "tos.dlg"
        path = importlib.resources.files(pkg)
        self.drama = Helpful()
        self.folder = SceneScript.Folder(
            pkg=pkg,
            description="Theatre of Spud",
            metadata={},
            paths=[i.name for i in path.glob("*.rst")],
            interludes=None
        )

    def test_pause(self):
        fn, args, kwargs = self.drama.interpret(self.drama.match("help"))
        results = list(self.drama(fn, *args, **kwargs))
        drama_dialogue = list(self.drama.build_dialogue(*results))
        n, presenter = Presenter.build_presenter(self.folder, *drama_dialogue, ensemble=self.drama.ensemble)
        self.assertEqual("pause.rst", self.folder.paths[n])
        self.assertIsInstance(presenter.frames[-1][Model.Line][-1].persona, Helpful, vars(presenter))

    def test_quit(self):
        fn, args, kwargs = self.drama.interpret(self.drama.match("quit"))
        results = list(self.drama(fn, *args, **kwargs))
        drama_dialogue = list(self.drama.build_dialogue(*results))
        n, presenter = Presenter.build_presenter(self.drama.folder, *drama_dialogue, ensemble=self.ensemble)
        self.assertEqual("quit.rst", self.folder.paths[n])
        self.assertIs(None, presenter.frames[-1][Model.Line][-1].persona, vars(presenter))
