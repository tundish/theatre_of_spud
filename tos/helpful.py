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
from collections import namedtuple

from turberfield.dialogue.model import SceneScript

from tos.types import NewDrama


class Helpful(NewDrama):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active.add(self.do_help)
        self.active.add(self.do_history)

    def pause(self):
        pass

    def do_help(self, this, text, /, **kwargs):
        """
        help | ?

        """
        self.pause()

        yield "[DRAMA]_"
        yield "You are woken early one Sunday morning."
        yield "Your flatmate is up and anxious."
        yield "Maybe you could make her a cup of tea."
        yield from super().do_help(this, text)
        yield "Start with a *look around*."
        yield "The character dialogue may give you some hints."
        yield "To see how things are coming along, you can *check* an object."
        yield "To see a list of past actions, use the *history* command."

    def do_history(self, this, text, /, **kwargs):
        """
        history

        """
        self.pause()
        yield "[DRAMA]_"
        yield "So far, it's been like this."
        yield from ("*{0.args[0]}*".format(i) for i in self.history)

    def do_hint(self, this, text, /, **kwargs):
        """
        hint

        """
        yield ""
