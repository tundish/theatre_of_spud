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

import random

from tos.mixins.moving import Moving
from tos.mixins.types import Awareness
from tos.mixins.types import Artifact
from tos.mixins.types import Significance


class Calls(Moving):
    """Taking phone calls"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, fn, *args, **kwargs):
        yield from super().__call__(fn, *args, **kwargs)

        phone = next(iter(self.lookup["phone"]))
        if phone.get_state(Significance) == Significance.indicate:
            yield random.choice([
                "Suddenly, the {0.name} rings.".format(phone),
                "The {0.name} starts to ring.".format(phone),
                "The {0.name} begins ringing.".format(phone),
            ])
        elif phone.get_state(Significance) in (
            Significance.emphasis, Significance.elevated, Significance.alarming
        ):
            yield random.choice([
                "The {0.name} rings again.".format(phone),
                "The {0.name} continues to ring.".format(phone),
                "The {0.name} is still ringing.".format(phone),
            ])

    def build(self, ensemble=None):
        yield from super().build()
        yield Artifact(
            names=["phone", "telephone"],
            detail={},
            messages=[],
        ).set_state(Awareness.ignorant)

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        phone = next(iter(self.lookup["phone"]))
        return rv
