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

from tos.map import Map
from tos.mixins.carrying import Carrying
from tos.mixins.moving import Moving
from tos.mixins.types import Awareness
from tos.mixins.types import Artifact


class Lights(Carrying, Moving):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active.add(self.do_lights_off)
        self.active.add(self.do_lights_on)

    def build(self):
        yield from super().build()
        yield Artifact(names=["lights"]).set_state(Awareness.ignorant, self.nav.Location.foyer, 1)
        yield Artifact(names=["fuse"]).set_state(Awareness.ignorant, self.nav.Location.lighting)

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        fuse = next(iter(self.lookup["fuse"]))
        lights = next(iter(self.lookup["lights"]))
        for obj in (fuse, lights):
            if self.player.get_state(self.nav.Location) == obj.get_state(self.nav.Location):
                if obj.get_state(Awareness) == Awareness.ignorant:
                    obj.state = Awareness.discover
                elif obj.get_state(Awareness) == Awareness.discover:
                    obj.state = Awareness.familiar

        if fuse.get_state(self.nav.Location) == self.nav.Location.foyer:
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
        next(iter(self.lookup["fuse"])).state = Awareness.complete
        next(iter(self.lookup["lights"])).state = Awareness.complete
        next(iter(self.lookup["lights"])).state = 1
        yield ""

    def do_lights_off(self, this, text, *args):
        """
        switch off lights | switch lights off
        turn off lights | turn lights off

        """
        lights = next(iter(self.lookup["lights"]))
        lights.state = 1
        if lights.get_state(Awareness) == Awareness.complete:
            yield "The exterior lights go out."

    def do_lights_on(self, this, text, *args):
        """
        switch on lights | switch lights on
        turn on lights | turn lights on

        """
        lights = next(iter(self.lookup["lights"]))
        lights.state = 2
        if lights.get_state(Awareness) == Awareness.complete:
            yield "The exterior lights come on."
