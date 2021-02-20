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

from tos.mixins.types import Motivation
from tos.mixins.types import Navigator
from tos.mixins.types import Proximity
from tos.mixins.types import NewDrama


class Moving(NewDrama):
    "Physical space"

    def __init__(self, nav: Navigator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nav = nav
        self.active.add(self.do_go)
        self.active.add(self.do_look)
        self.active.add(self.do_where)

    @property
    def location(self):
        locn = self.player.get_state(self.nav.Location)
        return random.choice(self.nav.scenery[locn.name])

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        mobs = [self.player] + [i for i in self.ensemble if hasattr(i, "state") and i is not self.player]
        for mob in mobs:
            if (mob.get_state(self.nav.Arriving)
                and mob.get_state(self.nav.Arriving).name != mob.get_state(self.nav.Location).name
            ):
                route = list(self.nav.route(
                    mob.get_state(self.nav.Location), mob.get_state(self.nav.Arriving)
                ))
                route.pop(0)
                if route:
                    mob.state = route[0]

            hops = list(self.nav.route(
                self.player.get_state(self.nav.Location), mob.get_state(self.nav.Location)
            ))
            mob.state = {
                0: Proximity.unknown, 1: Proximity.present, 2: Proximity.outside
            }.get(len(hops), Proximity.distant)
        return rv

    def do_go(self, this, text, /, *, locn: Navigator.__subclasses__()):
        """
        enter {locn.value[0]}
        enter {locn.value[1]}
        go {locn.value[0]} | go to {locn.value[0]}
        go {locn.value[1]} | go to {locn.value[1]}

        """
        self.player.state = self.player.get_state(self.nav.Location)
        self.player.state = self.nav.Departed[self.player.get_state(self.nav.Location).name]
        self.player.state = self.nav.Arriving[locn.name]
        yield f"{self.player.name} heads off to the {locn.value[0]}."

    def do_look(self, this, text, *args):
        """
        look | look around

        """
        locn = self.player.get_state(self.nav.Location)
        yield random.choice(["Exits are:", "We are close to:", "Nearby:"])
        yield from (
            "* the {0}".format(self.nav.Location[i].value[0].title()) for i in self.nav.topology[locn.name]
        )

    def do_where(self, this, text, *args):
        """
        where | where am i | where is it

        """
        locn = self.player.get_state(self.nav.Location)
        yield f"{self.player.name} is in the {locn.value[0]}."
