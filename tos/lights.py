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

import enum
import random

from turberfield.dialogue.types import EnumFactory

from tos.map import Map
from tos.mixins.carrying import Carrying
from tos.mixins.moving import Moving
from tos.mixins.types import Awareness
from tos.mixins.types import Artifact


@enum.unique
class Switch(EnumFactory, enum.Enum):
    broken = 0
    closed = 1
    opened = 2


class Lights(Carrying, Moving):
    """Operating lights"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self):
        yield from super().build()
        yield Artifact(
            names=["fuse"],
            detail={
                0: ["It's an inline fuse.", "It says, '13A'."],
            },
        ).set_state(Awareness.ignorant, self.nav.Location.lighting)
        yield Artifact(
            names=["lights"],
            detail={
                Switch.broken: ["There's empty slot here.", "The little neon lamp is out"],
                Switch.closed: ["The lights are on", "The switch is in the 'on' position."],
                Switch.opened: ["The lights are off", "The switch is in the 'off' position."],
            },
        ).set_state(Awareness.ignorant, self.nav.Location.foyer, Switch.broken)

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        fuse = next(iter(self.lookup["fuse"]))
        lights = next(iter(self.lookup["lights"]))
        for obj in (fuse, lights):
            if self.player.get_state(self.nav.Location) == obj.get_state(self.nav.Location):
                if obj is fuse:
                    self.active.add(self.do_get)
                else:
                    self.active.discard(self.do_get)
                if obj.get_state(Awareness) == Awareness.indicate:
                    self.active.add(self.do_lights_off)
                    self.active.add(self.do_lights_on)
                    obj.state = Awareness.discover
                elif obj.get_state(Awareness) == Awareness.discover:
                    obj.state = Awareness.familiar
                self.active.add(self.do_examine_lights)
            else:
                self.active.discard(self.do_examine_lights)

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
        next(iter(self.lookup["lights"])).state = random.choice([Switch.closed, Switch.opened])
        yield ""

    def do_lights_off(self, this, text, *args):
        """
        switch off lights | switch lights off
        turn off lights | turn lights off

        """
        lights = next(iter(self.lookup["lights"]))
        lights.state = Switch.opened
        if lights.get_state(Awareness) == Awareness.complete:
            yield "The exterior lights go out."

    def do_lights_on(self, this, text, *args):
        """
        switch on lights | switch lights on
        turn on lights | turn lights on

        """
        lights = next(iter(self.lookup["lights"]))
        lights.state = Switch.closed
        if lights.get_state(Awareness) == Awareness.complete:
            yield "The exterior lights come on."

    def do_examine_lights(self, this, text, /, *, obj:Artifact):
        """
        check {obj.names[0]}
        examine {obj.names[0]}

        """
        state = obj.get_state(Switch)
        yield random.choice(obj.detail[state])
