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
from collections import namedtuple
import importlib.resources
import re

from turberfield.catchphrase.presenter import Presenter
from turberfield.catchphrase.render import Action
from turberfield.catchphrase.render import Parameter
from turberfield.catchphrase.render import Renderer
from turberfield.catchphrase.render import Settings
from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.types import Stateful

import tos
from tos.acts import Act1
from tos.acts import Act2
from tos.map import Map
from tos.mixins.patrolling import Patrolling
from tos.mixins.types import Awareness
from tos.mixins.types import Character
from tos.mixins.types import Mode
from tos.types import Motivation

version = tos.__version__


Bookmark = namedtuple("Bookmark", ["package", "folder", "tally", "drama"])


class Story(Renderer, Stateful):
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

    @staticmethod
    def build_folder(pkg, **kwargs):
        path = importlib.resources.files(pkg)
        description = kwargs.get("description", "")
        return SceneScript.Folder(
            pkg=pkg,
            description=description,
            metadata={},
            paths=sorted(i.name for i in path.glob("*.rst")),
            interludes=None
        )

    def __init__(self, cfg=None, **kwargs):
        super().__init__()
        self.settings = Settings(**self.definitions)
        self.input = ""
        self.prompt = "?"
        self.refusal = "'{0}' is not an option right now."
        self.bookmarks = []
        self.state = 1
        self.dramas = {
            "tos.dlg.act1": Act1,
            "tos.dlg.act2": Act2,
        }

    @property
    def actions(self):
        yield Action(
            "cmd", None, "/{0.id.hex}/cmd/", [self.bookmark.drama.player], "post",
            [Parameter("cmd", True, self.validators["command"], [self.prompt], ">")],
            "Enter"
        )

    @property
    def bookmark(self):
        return self.bookmarks[0] if self.bookmarks else None

    def build(self, pkg=None, /, **kwargs):
        pkg = pkg or list(self.dramas.keys())[self.state - 1]
        folder = self.build_folder(pkg, **kwargs)
        drama = self.build_drama(pkg, **kwargs)
        bookmark = Bookmark(pkg, folder, Counter(), drama)
        self.bookmarks.insert(0, bookmark)
        return self.bookmark

    def build_drama(self, pkg, player_name="", **kwargs):
        ensemble = [
            Character(names=["Edward Lionheart"]).set_state(
                Awareness.ignorant, Motivation.leader, Map.Location.stage, 1
            )
        ]
        drama_class = self.dramas[pkg]
        drama = drama_class(Map())
        for obj in ensemble:
            obj.state = 1
            drama.add(obj)

        if player_name:
            drama.player = Character(
                names=[player_name]
            ).set_state(Mode.playing, drama.nav.Location.car_park, 1)
            for obj in drama.build(ensemble):
                drama.add(obj)
            drama.add(drama.player)

        for i in drama.lookup["fuse"]: i.state = drama.nav.Location.lighting
        for i in drama.lookup["lights"]: i.state = drama.nav.Location.foyer

        drama.patrols.update(drama.build_patrols(
            Patrolling.Patrol(
                next(iter(drama.lookup["Edward Lionheart"])),
                [drama.nav.Location.wings, drama.nav.Location.foyer],
                0
            )
        ))
        return drama

    def refresh_target(self, url):
        refresh_state = getattr(self.settings, "catchphrase-states-refresh", "inherit").lower()
        if refresh_state == "none":
            return None
        elif refresh_state == "inherit":
            return url
        else:
            return refresh_state

    def represent(self, lines=[]):
        presenter = Presenter.build_presenter(
            self.bookmark.folder, *lines,
            ensemble=self.bookmark.drama.ensemble + [self, self.bookmark.drama, self.settings],
            shot="Drama output"
        )
        if presenter and not(presenter.dwell or presenter.pause):
            setattr(self.settings, "catchphrase-reveal-extends", "none")
            setattr(self.settings, "catchphrase-states-scrolls", "scroll")
        else:
            setattr(self.settings, "catchphrase-reveal-extends", "both")
            setattr(self.settings, "catchphrase-states-scrolls", "visible")

        return presenter

    def update(self, index):
        bookmark = self.bookmark
        metadata = bookmark.drama.interlude(bookmark.folder, index)
        bookmark.folder.metadata.update(metadata)
        stem = bookmark.folder.paths[index].split(".")[0]
        bookmark.tally[stem] += 1
        pkg = list(self.dramas.keys())[self.state - 1]
        if pkg != bookmark.package:
            return self.build(pkg)
