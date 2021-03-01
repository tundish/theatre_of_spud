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

from collections import defaultdict
from collections import deque
import enum
import random

from turberfield.dialogue.types import DataObject
from turberfield.dialogue.types import EnumFactory
from turberfield.dialogue.types import Stateful


class Named(DataObject):

    @property
    def name(self):
        return random.choice(getattr(self, "names", [""]))


class Artifact(Named, Stateful): pass
class Character(Named, Stateful): pass


class Awareness(EnumFactory, enum.Enum):

    ignorant = enum.auto()
    indicate = enum.auto()
    discover = enum.auto()
    familiar = enum.auto()
    carrying = enum.auto()
    complete = enum.auto()


class Proximity(EnumFactory, enum.Enum):

    audible = enum.auto()
    distant = enum.auto()
    present = enum.auto()
    huddled = enum.auto()
    inbound = enum.auto()
    outside = enum.auto()
    outward = enum.auto()
    tactile = enum.auto()
    visible = enum.auto()
    unknown = enum.auto()
    whisper = enum.auto()


class Mode(EnumFactory, enum.Enum):

    default = enum.auto()
    develop = enum.auto()
    monitor = enum.auto()
    pausing = enum.auto()
    playing = enum.auto()
    preplay = enum.auto()
    success = enum.auto()
    testing = enum.auto()
    visitor = enum.auto()
    warning = enum.auto()


class Motion(EnumFactory, enum.Enum):

    broken = enum.auto()
    follow = enum.auto()
    leader = enum.auto()
    moving = enum.auto()
    patrol = enum.auto()
    routed = enum.auto()
    static = enum.auto()
    sticky = enum.auto()
