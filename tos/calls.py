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
from tos.mixins.types import Awareness
from tos.mixins.types import Artifact


class Calls(Moving):
    """Taking phone calls"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
