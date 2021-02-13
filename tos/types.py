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

import enum
import random
from types import SimpleNamespace

from turberfield.dialogue.types import DataObject
from turberfield.dialogue.types import EnumFactory
from turberfield.dialogue.types import Stateful


class Base(SimpleNamespace):

    classes = {}

    def transition(self, name, *args, **kwargs):
        self.classes[name] = type(name, args, {})
        data = self.__dict__.copy()
        data.update(kwargs)
        return self.classes[name](**data)


class Named(DataObject):

    @property
    def name(self):
        return random.choice(getattr(self, "names", [""]))


class Character(Named, Stateful): pass


class Motivation(EnumFactory, enum.Enum):

    acting = enum.auto()
    critic = enum.auto()
    friend = enum.auto()
    herald = enum.auto()
    murder = enum.auto()
    paused = enum.auto()
    player = enum.auto()
    profit = enum.auto()
    victim = enum.auto()


