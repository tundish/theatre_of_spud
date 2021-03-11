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

from collections import Counter
from collections.abc import Callable
import importlib.resources
import re

from turberfield.catchphrase.presenter import Presenter
from turberfield.catchphrase.render import Action
from turberfield.catchphrase.render import Parameter
from turberfield.catchphrase.render import Renderer
from turberfield.catchphrase.render import Settings
from turberfield.dialogue.model import SceneScript

# import logging
# logging.basicConfig(level=logging.DEBUG)

import tos
from tos.lights import Lights
from tos.map import Map
from tos.mixins.helpful import Helpful
from tos.mixins.patrolling import Patrolling
from tos.mixins.types import Awareness
from tos.mixins.types import Character
from tos.mixins.types import Mode
from tos.types import Motivation

version = tos.__version__


class Story(Renderer):
    """
    Some methods of this class are likely to end up in a later
    version of the Catchphrase library.

    You should keep a regular eye on https://github.com/tundish/turberfield-catchphrase
    to spot new releases.

    """

    definitions = {
        "catchphrase-colour-washout": "hsl(50, 0%, 100%, 1.0)",
        "catchphrase-colour-shadows": "hsl(202.86, 100%, 4.12%)",
        "catchphrase-colour-midtone": "hsl(203.39, 96.72%, 11.96%)",
        "catchphrase-colour-hilight": "hsl(203.06, 97.3%, 56.47%)",
        "catchphrase-colour-glamour": "hsl(353.33, 96.92%, 12.75%)",
        "catchphrase-colour-gravity": "hsl(293.33, 96.92%, 12.75%)",
        "catchphrase-reveal-extends": "both",
    }

    validators = {
        "command": re.compile("[\\w ]{1,36}"),
        "session": re.compile("[0-9a-f]{32}"),
        "player": re.compile("[A-Za-z]{2,24}")
    }


    class Act1(Lights, Patrolling, Helpful):

        @property
        def turns(self):
            return len([i for i in self.history
                        if i.fn not in (self.do_help, self.do_history, self.do_hint)])

    def __init__(self, cfg=None, **kwargs):
        self.acts = [self.Act1]
        self.settings = Settings(**self.definitions)
        self.drama = None
        self.folder = None
        self.index = None
        self.input = ""
        self.prompt = "?"
        self.refusal = "'{0}' is not an option right now."
        self.metadata = {}

    @property
    def actions(self):
        yield Action(
            "cmd", None, "/{0.id.hex}/cmd/", [self.drama.player], "post",
            [Parameter("cmd", True, self.validators["command"], [self.prompt], ">")],
            "Enter"
        )

    def load_drama(self, act=0, player_name="", ensemble=None):
        ensemble = ensemble or [
            Character(names=["Edward Lionheart"]).set_state(
                Awareness.ignorant, Motivation.leader, Map.Location.stage, 1
            )
        ]
        drama = self.acts[act](Map())

        for obj in ensemble:
            obj.state = 1
            drama.add(obj)

        if player_name:
            drama.player = Character(
                names=[player_name], tally=Counter()
            ).set_state(Mode.playing, Map.Location.car_park, 1)
            for obj in drama.build():
                drama.add(obj)
            drama.add(drama.player)

        drama.patrols.update(drama.build_patrols(
            Patrolling.Patrol(
                next(iter(drama.lookup["Edward Lionheart"])),
                [Map.Location.wings, Map.Location.foyer],
                0
            )
        ))
        return drama

    def load_folder(self, act=0):
        pkg = f"tos.dlg.act{act}"
        path = importlib.resources.files(pkg)
        return SceneScript.Folder(
            pkg=pkg,
            description="Theatre of Spud",
            metadata={},
            paths=sorted(i.name for i in path.glob("*.rst")),
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

    def represent(self, lines=[]):
        #if all(self.metadata.values()):
        #    act = self.metadata.get("act", 0)
        #    self.drama = self.load(act)
        #    self.metadata["act"] = act + 1

        self.index, presenter = Presenter.build_presenter(
            self.folder, *lines,
            ensemble=self.drama.ensemble + [self, self.drama, self.settings],
            shot="Drama output"
        )
        stem = self.folder.paths[self.index].split(".")[0]
        self.drama.player.tally[stem] += 1
        if presenter and not(presenter.dwell or presenter.pause):
            setattr(self.settings, "catchphrase-reveal-extends", "none")
            setattr(self.settings, "catchphrase-states-scrolls", "scroll")
        else:
            setattr(self.settings, "catchphrase-reveal-extends", "both")
            setattr(self.settings, "catchphrase-states-scrolls", "visible")

        return presenter
