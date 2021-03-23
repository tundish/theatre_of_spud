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

import random

from tos.calls import Calls
from tos.knowledge import Knowledge
from tos.lights import Lights
from tos.map import Map
from tos.mixins.helpful import Helpful
from tos.mixins.moving import Moving
from tos.mixins.patrolling import Patrolling
from tos.mixins.telegraph import Telegraph
from tos.mixins.types import Awareness
from tos.mixins.types import Artifact
from tos.mixins.types import Character
from tos.mixins.types import Mode
from tos.mixins.types import Significance
from tos.types import Motivation


class FirstPositions:

    def build(self, ensemble=None, **kwargs):
        yield from super().build(ensemble)

        yield Character(names=["Edward Lionheart"]).set_state(
            Awareness.ignorant, Motivation.leader, self.nav.Location.corridor
        )

        player_name = kwargs.get("player_name", "Alan")
        self.player = Character(names=[player_name]).set_state(Mode.playing, self.nav.Location.car_park)
        yield self.player


class Act01(FirstPositions, Lights, Patrolling, Helpful):

    @property
    def turns(self):
        return len([i for i in self.history
                    if i.fn not in (self.do_help, self.do_history, self.do_hint)])

    def build(self, ensemble=None, **kwargs):
        for obj in super().build(ensemble):
            if "fuse" in getattr(obj, "names", []): obj.state = self.nav.Location.lighting
            if "lights" in getattr(obj, "names", []): obj.state = self.nav.Location.foyer

            if "Edward Lionheart" in obj.names:
                self.patrols.update(self.build_patrols(
                    Patrolling.Patrol(
                        obj, [self.nav.Location.wings, self.nav.Location.foyer], 1)
                ))

            yield obj


class Act02(FirstPositions, Calls, Helpful):

    def __call__(self, fn, *args, **kwargs):
        phone = next(iter(self.lookup["phone"]))
        for line in super().__call__(fn, *args, **kwargs):
            if "ring" in line and not phone.state % 2:
                continue
            else:
                yield line

    def build(self, ensemble=None, **kwargs):
        for obj in super().build(ensemble):
            if obj.get_state(Mode) == Mode.playing:
                obj.state = self.nav.Location.foyer

            if "phone" in getattr(obj, "names", []):
                obj.detail.update({
                    0: ["The telephone is mounted on the wall.", "It's a grey rotary telephone."],
                    Significance.indicate: ["The phone is ringing."],
                })
                self.messengers.update({
                    obj: Telegraph.Messenger(obj, [
                        Knowledge.Message(
                            Knowledge.Noun("Angela Grant", "f"), (Knowledge.Noun("Danny", "m"),),
                            ("{nouns[0].name} is going to the football",
                             "{nouns[0].name}'s Dad has got tickets to the football"),
                            ("{nouns[0].name} is at Fellows Park",
                             "{nouns[0].name} can't do the play tonight",
                            ),
                            ("officer", "danny")
                        ),
                        Knowledge.Message(
                            Knowledge.Noun("Sarah Scott", "f"), (Knowledge.Noun("Michael", "m"),),
                            ("{nouns[0].name} is going to the football",
                             "{nouns[0].name}'s Dad has got tickets to the football"),
                            ("{nouns[0].name} is at Fellows Park",
                             "{nouns[0].name} can't do the play tonight",
                            ),
                            ("bluntschli", "michael")
                        ),
                        Knowledge.Message(
                            Knowledge.Noun("Paul Robbins", "m"), (Knowledge.Noun("Hayley", "f"),),
                            ("{nouns[0].name} is going to the football",
                             "{nouns[0].name}'s Dad has got tickets to the football"),
                            ("{nouns[0].name} is at Fellows Park",
                             "{nouns[0].name} can't do the play tonight",
                            ),
                            ("louka", "hayley")
                        ),
                    ], 1, period=2)
                })
                obj.state = self.nav.Location.office

            yield obj

    def do_go(self, this, text, /, *args, locn: Map.Location):
        """
        enter {locn.value[0]}
        enter {locn.value[1]}
        enter {locn.value[2]}
        go {locn.value[0]} | go to {locn.value[0]}
        go {locn.value[1]} | go to {locn.value[1]}
        go {locn.value[2]} | go to {locn.value[2]}

        """
        yield from super().do_go(this, text, locn=locn)

    def do_look(self, this, text, *args):
        """
        look | look around

        """
        yield from super().do_look(this, text, *args)
        artifacts = [
            i for i in self.ensemble
            if isinstance(i, Artifact)
            and self.player.get_state(self.nav.Location) == i.get_state(self.nav.Location)
        ]
        if artifacts:
            yield random.choice(["In view:", "We can see:"])
            yield from ("* {0.names[0]}".format(i) for i in artifacts)
