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

import argparse
import sys
import time

# import logging
# logging.basicConfig(level=logging.DEBUG)

from tos.move import Location
from tos.types import Character
from tos.types import Motivation

from tos.story import Story


def parser():
    return argparse.ArgumentParser()


def main(args):
    name = input("Enter your character's first name: ") or "Francis"
    story = Story(**vars(args))
    story.drama.add(Character(names=[name]).set_state(Motivation.player, Location.car_park))
    lines = []
    while story.drama.active:
        presenter = story.represent(lines)
        for frame in presenter.frames:
            animation = presenter.animate(frame, dwell=presenter.dwell, pause=presenter.pause)
            if not animation:
                continue
            for line, duration in story.render_frame_to_terminal(animation):
                print(line, "\n")
                time.sleep(duration)

        else:

            if story.drama.outcomes["finish"]:
                break

            story.input = input("{0} ".format(story.prompt))
            fn, args, kwargs = story.drama.interpret(story.drama.match(story.input))
            lines = list(story.drama(fn, *args, **kwargs))

def run():
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)


if __name__ == "__main__":
    run()
