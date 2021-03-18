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

from tos.calls import Calls
from tos.lights import Lights
from tos.mixins.helpful import Helpful
from tos.mixins.patrolling import Patrolling
from tos.mixins.types import Awareness
from tos.mixins.types import Character
from tos.mixins.types import Mode
from tos.types import Motivation


class Act1(Lights, Patrolling, Helpful):

    @property
    def turns(self):
        return len([i for i in self.history
                    if i.fn not in (self.do_help, self.do_history, self.do_hint)])

    def build(self, ensemble=None, **kwargs):
        for obj in super().build(ensemble):
            if "fuse" in getattr(obj, "names", []): obj.state = self.nav.Location.lighting
            if "lights" in getattr(obj, "names", []): obj.state = self.nav.Location.foyer

            yield obj

        ed = Character(names=["Edward Lionheart"]).set_state(
            Awareness.ignorant, Motivation.leader, self.nav.Location.wings, 1
        )
        self.patrols.update(self.build_patrols(
            Patrolling.Patrol(
                ed, [self.nav.Location.wings, self.nav.Location.foyer], 0)
        ))
        yield ed

        player_name = kwargs.get("player_name", "Alan")
        self.player = Character(names=[player_name]).set_state(Mode.playing, self.nav.Location.car_park, 1)
        yield self.player



class Act2(Calls, Patrolling, Helpful):

    def build(self, ensemble=None, **kwargs):
        yield from super().build(ensemble)
