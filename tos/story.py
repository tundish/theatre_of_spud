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

from collections.abc import Callable

from turberfield.catchphrase.presenter import Presenter
from turberfield.catchphrase.render import Renderer
from turberfield.catchphrase.render import Settings
from turberfield.dialogue.model import SceneScript

# import logging
# logging.basicConfig(level=logging.DEBUG)

import tos
from tos.moves import Location
from tos.moves import Moves
from tos.types import Character
from tos.types import Motivation

version = tos.__version__


class Story(Renderer):
    """
    Some methods of this class are likely to end up in a later
    version of the Catchphrase library.

    You should keep a regular eye on https://github.com/tundish/turberfield-catchphrase
    to spot new releases.

    """

    classes = {}

    def __init__(self, cfg=None, **kwargs):
        self.definitions = {
            "catchphrase-colour-washout": "hsl(50, 0%, 100%, 1.0)",
            "catchphrase-colour-shadows": "hsl(202.86, 100%, 4.12%)",
            "catchphrase-colour-midtone": "hsl(203.39, 96.72%, 11.96%)",
            "catchphrase-colour-hilight": "hsl(203.06, 97.3%, 56.47%)",
            "catchphrase-colour-glamour": "hsl(353.33, 96.92%, 12.75%)",
            "catchphrase-colour-gravity": "hsl(293.33, 96.92%, 12.75%)",
            "catchphrase-reveal-extends": "both",
        }
        self.settings = Settings(**self.definitions)
        self.folder = None
        self.input = ""
        self.prompt = "?"
        self.act = 1

    @property
    def act(self):
        return self.drama.act

    @act.setter
    def act(self, val):
        if val == 1:
            self.drama = self.transition("Act1", Moves, act=1)
            self.folder = SceneScript.Folder(
                pkg="tos.dlg",
                description="Theatre of Spud",
                metadata={},
                paths=["enter.rst", "lionheart.rst", "standin.rst", "pause.rst", "quit.rst"],
                interludes=None
            )

    @property
    def player(self):
        return self.drama.player

    @player.setter
    def player(self, name):
        self.drama.player = Character(names=[name]).set_state(Motivation.player, Location.car_park)
        self.drama.add(self.drama.player)

    def transition(self, name, *args, **kwargs):
        self.classes[name] = type(name, args, {})
        data = self.__dict__.copy()
        data.update(kwargs)
        return self.classes[name](**data)

    def refresh_target(self, url):
        refresh_state = getattr(self.settings, "catchphrase-states-refresh", "inherit").lower()
        if refresh_state == "none":
            return None
        elif refresh_state == "inherit":
            return url
        else:
            return refresh_state

    def represent(self, lines=[], index=None, loop=None):
        metadata = self.drama.interlude(self.folder, index, loop=loop)

        n, presenter = Presenter.build_presenter(
            self.folder, *lines,
            ensemble=self.drama.ensemble + [self, self.settings]
        )
        if presenter and not(presenter.dwell or presenter.pause):
            setattr(self.settings, "catchphrase-reveal-extends", "none")
            setattr(self.settings, "catchphrase-states-scrolls", "scroll")
        else:
            setattr(self.settings, "catchphrase-reveal-extends", "both")
            setattr(self.settings, "catchphrase-states-scrolls", "visible")

        return presenter
