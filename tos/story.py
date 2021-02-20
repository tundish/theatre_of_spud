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
import importlib.resources

from turberfield.catchphrase.presenter import Presenter
from turberfield.catchphrase.render import Renderer
from turberfield.catchphrase.render import Settings
from turberfield.dialogue.model import SceneScript

# import logging
# logging.basicConfig(level=logging.DEBUG)

import tos
from tos.map import Map
from tos.mixins.directing import Directing
from tos.mixins.helpful import Helpful
from tos.mixins.moving import Moving
from tos.mixins.types import Character
from tos.mixins.types import Motivation

version = tos.__version__


class Story(Renderer):
    """
    Some methods of this class are likely to end up in a later
    version of the Catchphrase library.

    You should keep a regular eye on https://github.com/tundish/turberfield-catchphrase
    to spot new releases.

    """

    class Act1(Directing, Moving, Helpful): pass

    def __init__(self, cfg=None, **kwargs):
        self.acts = [self.Act1]
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
        self.drama = None
        self.folder = None
        self.input = ""
        self.prompt = "?"
        self.metadata = {}

    def load_drama(self, act=0, player_name="", ensemble=None):
        ensemble = ensemble or []
        drama = self.acts[act](Map())

        for obj in ensemble:
            drama.add(obj)

        if player_name:
            for obj in drama.build():
                drama.add(obj)
            drama.add(Character(names=[player_name]).set_state(Motivation.player, Map.Location.car_park))

        drama.player = drama.ensemble[-1]
        return drama

    def load_folder(self, act=0):
        pkg = f"tos.dlg.act{act}"
        path = importlib.resources.files(pkg)
        return SceneScript.Folder(
            pkg=pkg,
            description="Theatre of Spud",
            metadata={},
            paths=[i.name for i in path.glob("*.rst")],
            interludes=None
        )

    def refresh_target(self, url):
        refresh_state = getattr(self.settings, "catchphrase-states-refresh", "inherit").lower()
        if refresh_state == "none":
            return None
        elif refresh_state == "inherit":
            return url
        else:
            return refresh_state

    def represent(self, lines=[], index=None, loop=None):
        #if all(self.metadata.values()):
        #    act = self.metadata.get("act", 0)
        #    self.drama = self.load(act)
        #    self.metadata["act"] = act + 1

        self.metadata.update(self.drama.interlude(self.folder, index, loop=loop))
        # if "act" in metadata

        n, presenter = Presenter.build_presenter(
            self.folder, *lines,
            ensemble=self.drama.ensemble + [self, self.drama, self.settings],
            shot="Drama output"
        )
        if presenter and not(presenter.dwell or presenter.pause):
            setattr(self.settings, "catchphrase-reveal-extends", "none")
            setattr(self.settings, "catchphrase-states-scrolls", "scroll")
        else:
            setattr(self.settings, "catchphrase-reveal-extends", "both")
            setattr(self.settings, "catchphrase-states-scrolls", "visible")

        return presenter
