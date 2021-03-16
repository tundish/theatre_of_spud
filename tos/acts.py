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


class Act1(Lights, Patrolling, Helpful):

    @property
    def turns(self):
        return len([i for i in self.history
                    if i.fn not in (self.do_help, self.do_history, self.do_hint)])

class Act2(Calls, Patrolling, Helpful):
    pass
