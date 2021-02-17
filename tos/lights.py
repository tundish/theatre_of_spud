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

from tos.moving import Departed
from tos.moving import Location
from tos.moving import Moving
from tos.types import Aware
from tos.types import Artifact


class Carrying:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active.add(self.do_get)

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        mobs = [
            i for i in self.ensemble
            if hasattr(i, "state") and i.get_state(Aware) == Aware.carrying
        ]
        for mob in mobs:
            mob.state = self.player.get_state(Location)
        return rv

    def do_get(self, this, text, /, *, obj: Artifact):
        """
        get {obj.names[0]}
        pick up {obj.names[0]}

        """
        locn = self.player.get_state(Location)
        if obj.get_state(Location) != locn:
            yield f"There is no {obj.name} here."
            return

        obj.state = Departed[locn.name]
        obj.state = Aware.carrying


class Lights(Carrying, Moving):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active.add(self.do_lights_off)
        self.active.add(self.do_lights_on)

    def build(self):
        yield from super().build()
        yield Artifact(names=["lights"]).set_state(Aware.ignorant, Location.foyer, 1)
        yield Artifact(names=["fuse"]).set_state(Aware.ignorant, Location.lighting)

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        fuse = next(iter(self.lookup["fuse"]))
        lights = next(iter(self.lookup["lights"]))
        for obj in (fuse, lights):
            if self.player.get_state(Location) == obj.get_state(Location):
                if obj.get_state(Aware) == Aware.ignorant:
                    obj.state = Aware.discover
                elif obj.get_state(Aware) == Aware.discover:
                    obj.state = Aware.familiar

        if fuse.get_state(Location) == Location.foyer:
            self.active.add(self.do_fit_fuse)
        else:
            self.active.discard(self.do_fit_fuse)
        return rv

    def do_fit_fuse(self, this, text, *args):
        """
        fit fuse
        fit fuse in light
        put fuse in slot

        """
        next(iter(self.lookup["fuse"])).state = Aware.complete
        next(iter(self.lookup["lights"])).state = Aware.complete
        next(iter(self.lookup["lights"])).state = 1
        yield ""

    def do_lights_off(self, this, text, *args):
        """
        switch off lights | switch lights off
        turn off lights | turn lights off

        """
        lights = next(iter(self.lookup["lights"]))
        lights.state = 1
        if lights.get_state(Aware) == Aware.complete:
            yield "The exterior lights go out."

    def do_lights_on(self, this, text, *args):
        """
        switch on lights | switch lights on
        turn on lights | turn lights on

        """
        lights = next(iter(self.lookup["lights"]))
        lights.state = 2
        if lights.get_state(Aware) == Aware.complete:
            yield "The exterior lights come on."
