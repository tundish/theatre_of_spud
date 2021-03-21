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

import unittest

from tos.mixins.types import Artifact
from tos.mixins.types import Significance
from tos.mixins.types import Proximity
from tos.mixins.patrolling import Patrolling

from tos.mixins.test.test_moving import TestTrack


from collections import deque
from collections import namedtuple
from turberfield.catchphrase.drama import Drama

class Telegraph(Drama):

    Messenger = namedtuple("Messenger", ["npc", "messages", "pending", "period"])

    @staticmethod
    def build_messengers(*args):
        return {i.npc: i for i in args}

    def __init__(self, *args, messengers=[], **kwargs):
        super().__init__(*args, **kwargs)
        self.messengers = self.build_messengers(*messengers)

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        for i in self.messengers:
            if not i.get_state(Significance):
                i.state = Significance.notknown
            elif i.get_state(Significance) == Significance.indicate:
                i.state = Significance.emphasis
            elif i.get_state(Significance) == Significance.silenced:
                continue

            messenger = self.messengers[i]
            n = messenger.pending
            if not n:
                state = i.get_state(Significance)
                if state in (Significance.notknown, Significance.inactive):
                    i.state = Significance.indicate
                elif state == Significance.declined:
                    i.state = Significance.inactive
                elif state == Significance.accepted:
                    i.state = Significance.inactive
                    n = messenger.period
                    try:
                        messenger.messages.rotate(-1)
                    except AttributeError:
                        messenger.messages.pop(0)
            else:
                n -= 1

            self.messengers[i] = self.messengers[i]._replace(pending=n)
        return rv


class TestTelegraph(unittest.TestCase):

    def setUp(self):
        self.drama = Telegraph()

    def test_modes(self):
        a = Artifact(names=["joke book"])
        b = Artifact(names=["news channel"])
        self.drama.messengers = {
            a: Telegraph.Messenger(a, ["englishman", "irishman", "scotsman"], 4, period=1),
            b: Telegraph.Messenger(a, deque(["headlines", "weather", "sport"]), 0, period=3)
        }
        for n in range(28):
            metadata = self.drama.interlude(None, None)
            with self.subTest(n=n, msgs=self.drama.messengers):
                if n == 0:
                    self.assertEqual(2, len(self.drama.messengers))
                    self.assertEqual(Significance.notknown, a.get_state(Significance))
                    self.assertEqual(Significance.indicate, b.get_state(Significance))
                    self.assertEqual("headlines", self.drama.messengers[b].messages[0])
                elif n == 1:
                    self.assertEqual(Significance.notknown, a.get_state(Significance))
                    self.assertEqual(Significance.emphasis, b.get_state(Significance))
                    self.assertEqual("headlines", self.drama.messengers[b].messages[0])
                    b.state = Significance.accepted
                elif n == 2:
                    self.assertEqual(Significance.notknown, a.get_state(Significance))
                    self.assertEqual(Significance.inactive, b.get_state(Significance))
                    self.assertEqual("weather", self.drama.messengers[b].messages[0])
                elif n == 4:
                    self.assertEqual(Significance.indicate, a.get_state(Significance))
                    self.assertEqual(Significance.inactive, b.get_state(Significance))
                    self.assertEqual("weather", self.drama.messengers[b].messages[0])
                elif n == 5:
                    self.assertEqual(Significance.emphasis, a.get_state(Significance))
                    self.assertEqual(Significance.inactive, b.get_state(Significance))
                    self.assertEqual("englishman", self.drama.messengers[a].messages[0])
                    a.state = Significance.accepted
                elif n == 6:
                    self.assertEqual(Significance.inactive, a.get_state(Significance))
                    self.assertEqual("irishman", self.drama.messengers[a].messages[0])
                elif n == 7:
                    self.assertEqual(Significance.indicate, a.get_state(Significance))
                    self.assertEqual("irishman", self.drama.messengers[a].messages[0])
                    a.state = Significance.declined
                elif n == 8:
                    self.assertEqual(Significance.indicate, a.get_state(Significance))
                    self.assertEqual("irishman", self.drama.messengers[a].messages[0])
                    a.state = Significance.accepted
                elif n == 12:
                    self.assertEqual(1, len(self.drama.messengers))
