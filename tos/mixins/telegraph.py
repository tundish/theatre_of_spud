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

from collections import namedtuple

from turberfield.catchphrase.drama import Drama

from tos.mixins.types import Significance


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
        for i in list(self.messengers.keys()):
            if not i.get_state(Significance):
                i.state = Significance.notknown
            elif i.get_state(Significance) == Significance.indicate:
                i.state = Significance.emphasis
            elif i.get_state(Significance) == Significance.suppress:
                continue

            messenger = self.messengers[i]
            if not messenger.messages:
                del self.messengers[i]
                continue

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
