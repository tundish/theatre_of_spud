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
    critic = enum.auto()
    friend = enum.auto()
    herald = enum.auto()
    murder = enum.auto()
    paused = enum.auto()
    player = enum.auto()
    profit = enum.auto()
    victim = enum.auto()


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
        "balcony": ["auditorium", "bar"],
        "bar": ["foyer", "kitchen", "stairs", "passage"],
        "car_park": ["foyer"],
        "cloaks": ["foyer"],
        "corridor": ["auditorium", "foyer", "wings"],
        "costume": ["backstage", "wings"],
        "foyer": ["car_park", "corridor", "office", "cloaks", "bar"],
        "kitchen": ["bar"],
        "lighting": ["balcony", "stairs"],
        "office": ["foyer"],
        "passage": ["auditorium", "bar", "wings"],
        "stage": ["wings"],
        "stairs": ["auditorium", "balcony", "bar", "lighting"],
        "wings": ["backstage", "corridor", "costume", "passage", "stage"],
    }


    routes = {}

    def route(self, dest):
        if (self.name, dest.name) in self.routes:
            return self.routes[(self.name, dest.name)]

        typ = type(self)
        rvs = set()
        paths = [[self]]
        n = len(self.topology)
        d = 1
        while n >= 0 or not rvs:
            nxt = []
            for p in paths:
                if p[-1].name == dest.name:
                    rvs.add(tuple(p))
                else:
                    nodes = self.topology[p[-1].name]
                    d = len(nodes)
                    for i in nodes:
                        nxt.append(p.copy())
                        nxt[-1].append(typ[i])
            paths = nxt
            n = n - d

        rv = sorted(rvs, key=len)[0] if rvs else []
        self.routes[(self.name, dest.name)] = rv
        return rv

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
            paths=["enter.rst", "lionheart.rst", "standin.rst", "pause.rst", "quit.rst"],
            interludes=self.interlude
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = None
        self.outcomes = defaultdict(bool)
        self.active.add(self.do_go)
        self.active.add(self.do_look)

    def __call__(self, fn, *args, **kwargs):
        self.player = next(
            (i for i in self.ensemble if hasattr(i, "state") and i.get_state(Motivation) == Motivation.player),
            None
        )
        yield from super().__call__(fn, *args, **kwargs)

    def interlude(self, folder, index, **kwargs):
        mobs = [
            i for i in self.ensemble
            if hasattr(i, "state") and i.get_state(Arriving)
            and i.get_state(Arriving).name != i.get_state(Location).name
        ]
        for mob in mobs:
            route = list(Location.route(mob.get_state(Location), mob.get_state(Arriving)))
            route.pop(0)
            if route:
                mob.state = route[0]
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
        self.player.state = self.player.get_state(Location) or Location.car_park
        self.player.state = Departed[self.player.get_state(Location).name]
        self.player.state = locn
        yield "OK off we go"

    def do_look(self, this, text, *args):
        """
        look | look around
        where | where am i | where is it

        """
        locn = self.player.get_state(Location)
        yield f"{self.player.name} is in the {locn.value[0]}."
        yield random.choice(["Exits are:", "We are close to:", "Nearby:"])
        yield from ("* the {0}".format(Location[i].value[0].title()) for i in locn.topology[locn.name])

