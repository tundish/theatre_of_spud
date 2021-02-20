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

from tos.mixins.moving import Moving
from tos.mixins.types import Artifact
from tos.mixins.types import Awareness


class Carrying(Moving):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active.add(self.do_get)

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        mobs = [
            i for i in self.ensemble
            if hasattr(i, "state") and i.get_state(Awareness) == Awareness.carrying
        ]
        for mob in mobs:
            mob.state = self.player.get_state(self.nav.Location)
        return rv

    def do_get(self, this, text, /, *, obj: Artifact):
        """
        get {obj.names[0]}
        pick up {obj.names[0]}

        """
        locn = self.player.get_state(self.nav.Location)
        if obj.get_state(self.nav.Location) != locn:
            yield f"There is no {obj.name} here."
            return

        obj.state = self.nav.Departed[locn.name]
        obj.state = Awareness.carrying
