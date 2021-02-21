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

from turberfield.catchphrase.drama import Drama
from turberfield.dialogue.types import DataObject
from turberfield.dialogue.types import EnumFactory
from turberfield.dialogue.types import Stateful


class NewDrama(Drama):

    def __init__(self, **kwargs):
        self.lookup = defaultdict(set)
        self.active = set()
        self.history = deque()

    def __call__(self, fn, *args, **kwargs):
        lines = list(fn(fn, *args, **kwargs))
        self.history.appendleft(self.Record(fn, args, kwargs, lines))
        yield from lines

    @property
    def ensemble(self):
        return list({i for s in self.lookup.values() for i in s})

    @property
    def turns(self):
        return len(self.history)

    def build(self):
        yield from []

    def add(self, *args):
        for item in args:
            for n in getattr(item, "names", []):
                self.lookup[n].add(item)

    def interlude(self, folder, index, **kwargs) -> dict:
        return {}

    def interpret(self, options):
        return next(iter(options), "")


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
    outside = enum.auto()
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
