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

from collections import namedtuple

from tos.mixins.moving import Moving
from tos.mixins.types import Mode


class Patrolling(Moving):

    Patrol = namedtuple("Patrol", ["npc", "orders", "pos"])

    def __init__(self, *args, patrols=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.patrols = {i.npc: i for i in patrols or []}

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        for c, p in self.patrols.items():
            if c.get_state(Mode) == Mode.pausing:
                continue

            pos = p.pos or 0
            hop = p.orders[pos]
            locn = c.get_state(self.nav.Location)
            c.state = locn or self.nav.Location[hop.name]

            dst = c.get_state(self.nav.Arriving)
            if not dst or dst.name != hop.name:
                c.state = self.nav.Arriving[hop.name]

            locn = c.get_state(self.nav.Location)
            if locn.name == c.get_state(self.nav.Arriving).name:
                c.state = self.nav.Departed[locn.name]
                self.patrols[c] = p._replace(pos=(pos + 1) % len(p.orders))
        return rv
