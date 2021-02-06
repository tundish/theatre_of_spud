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

import enum

from turberfield.catchphrase.drama import Drama
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
        "box_office": ["box office", "office"],
        "car_park": ["car park"],
        "cloakroom": ["cloakroom"],
        "costume": ["costume store", "props room"],
        "backstage": ["backstage"],
        "foyer": ["foyer"],
        "kitchen": ["kitchen"],
        "lighting box": ["lighting box"],
        "stage left": ["wings", "stage left"],
        "stage right": ["wings", "stage right"],
    }

Arriving = enum.Enum("Arriving", Navigator.spots, type=Navigator)
Departed = enum.Enum("Departed", Navigator.spots, type=Navigator)
Location = enum.Enum("Location", Navigator.spots, type=Navigator)


class Stage(Drama):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active.add(self.do_go)

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
