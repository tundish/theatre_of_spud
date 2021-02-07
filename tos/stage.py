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

from collections import defaultdict
from collections import deque
import enum
import functools
import random

from turberfield.catchphrase.drama import Drama
from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.types import DataObject
from turberfield.dialogue.types import EnumFactory
from turberfield.dialogue.types import Stateful


class Motivation(enum.Enum):

    acting = enum.auto()
    paused = enum.auto()
    player = enum.auto()
    herald = enum.auto()


class Named(DataObject):

    @property
    def name(self):
        return random.choice(getattr(self, "names", [""]))


class Character(Named, Stateful): pass


class Navigator(EnumFactory):

    spots = {
        "auditorium": ["auditorium"],
        "backstage": ["backstage"],
        "balcony": ["balcony", "downstairs"],
        "bar": ["bar"],
        "car_park": ["car park"],
        "cloaks": ["cloakroom", "cloaks"],
        "corridor": ["corridor"],
        "costume": ["costume store", "props room"],
        "foyer": ["foyer"],
        "kitchen": ["kitchen"],
        "lighting": ["lighting box"],
        "office": ["box office", "office"],
        "passage": ["passage"],
        "stage": ["stage", "onstage"],
        "stairs": ["stairs", "upstairs"],
        "wings": ["wings", "stage left", "stage right"],
    }

    topology = {
        "auditorium": ["balcony", "corridor", "passage"],
        "backstage": ["costume", "wings"],
        "balcony": ["bar"],
        "bar": ["kitchen", "stairs", "passage"],
        "car_park": ["foyer"],
        "cloaks": ["foyer"],
        "corridor": ["auditorium", "foyer", "wings"],
        "costume": ["backstage", "wings"],
        "foyer": ["corridor", "office", "cloaks", "bar"],
        "kitchen": ["bar"],
        "lighting": ["balcony"],
        "office": ["foyer"],
        "passage": ["auditorium", "bar", "wings"],
        "stage": ["wings"],
        "stairs": ["lighting", "auditorium"],
        "wings": ["backstage", "costume", "stage"],
    }


    routes = {
    }

    def route(self, dest, maxlen, crumbs=None, visited=None):
        try:
            return self.routes[(self, dest)]
        except KeyError:
            return None

        crumbs = crumbs or deque([], maxlen=maxlen)
        visited = set([]) if visited is None else set(visited)

        paths = self.topology[self.name]
        for path in paths:
            hop = type(self)[path]
            if path.name == dest.name:
                return crumbs

            if hop not in visited:
                visited.add(hop)
                try:
                    rv = deque(hop.route(dest, maxlen, crumbs, frozenset(visited)))
                    rv.appendleft(hop)
                except TypeError:
                    continue

            if len(rv) != maxlen:
                return rv
        else:
            return None

Arriving = enum.Enum("Arriving", Navigator.spots, type=Navigator)
Departed = enum.Enum("Departed", Navigator.spots, type=Navigator)
Location = enum.Enum("Location", Navigator.spots, type=Navigator)


class Stage(Drama):

    @property
    def folder(self):
        return SceneScript.Folder(
            pkg="tos.dlg",
            description="Theatre of Spud",
            metadata={},
            paths=["lionheart.rst", "standin.rst", "pause.rst", "quit.rst"],
            interludes=self.interlude
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.outcomes = defaultdict(bool)
        self.active.add(self.do_go)

    def interlude(self, folder, index, **kwargs):
        # When player heads to telephone, L goes backstage
        # When player comes from telephone, L goes to foyer
        return {}

    def do_go(self, this, text, /, *, locn: Arriving):
        """
        go {locn.value[0]} | go to {locn.value[0]} | enter {locn.value[0]}
        run {locn.value[0]} | run to {locn.value[0]}
        go {locn.value[1]} | go to {locn.value[1]} | enter {locn.value[1]}
        run {locn.value[1]} | run to {locn.value[1]}

        """
        player = next(i for i in self.ensemble if hasattr(i, "state") and i.get_state(Motivation) == Motivation.player)
        player.state = player.get_state(Location) or Location.car_park
        player.state = Departed[player.get_state(Location).name]
        player.state = locn
        yield ""
