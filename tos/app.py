#!/usr/bin/env python3
# encoding: utf-8

# This is a technical demo and teaching example for the turberfield-catchphrase library.
# Copyright (C) 2021 D. Haynes

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
from collections import deque
import importlib.resources
import logging
import sys
import uuid

from aiohttp import web
import pkg_resources

from turberfield.catchphrase.presenter import Presenter

import tos
from tos.story import Story


async def get_frame(request):
    try:
        uid = uuid.UUID(hex=request.match_info["story"])
        story = request.app["stories"][uid]
    except (KeyError, ValueError):
        raise web.HTTPNotFound(reason="User sent invalid command.")
    else:
        log = logging.getLogger("tos.{0!s}".format(uid))

    try:
        animation = None
        while not animation:
            frame = story.presenter.frames.pop(0)
            animation = story.presenter.animate(frame, dwell=story.presenter.dwell, pause=story.presenter.pause)
            log.info(animation)
    except (AttributeError, IndexError):
        story.presenter = story.represent()
        frame = story.presenter.frames.pop(0)
        animation = story.presenter.animate(frame)

    refresh = Presenter.refresh_animations(animation, min_val=2) if story.presenter.pending else None
    refresh_target = "/{0.hex}".format(uid) if story.drama.active else None

    title = next(iter(story.presenter.metadata.get("project", ["Theatre Of Spud"])), "Theatre Of Spud")
    controls = [
        "\n".join(story.render_action_form(action, autofocus=not n))
        for n, action in enumerate(story.actions)
        if not story.presenter.pending
    ]
    rv = story.render_body_html(title=title, next_=refresh_target, refresh=refresh).format(
        '<link rel="stylesheet" href="/css/theme/tos.css" />',
        story.render_dict_to_css(vars(story.settings)),
        story.render_animated_frame_to_html(animation, controls)
    )
    log.info("Turn {0.drama.turns}".format(story))
    return web.Response(text=rv, content_type="text/html")


async def post_command(request):
    try:
        uid = uuid.UUID(hex=request.match_info["story"])
        story = request.app["stories"][uid]
    except (KeyError, ValueError):
        raise web.HTTPNotFound(reason="Invalid story id.")
    else:
        log = logging.getLogger("tos.{0!s}".format(uid))

    story = request.app["stories"][uid]
    data = await request.post()
    cmd = data["cmd"]
    if not story.validators["command"].match(cmd):
        raise web.HTTPUnauthorized(reason="User sent invalid command.")

    story.input = cmd
    fn, args, kwargs = story.drama.interpret(story.drama.match(cmd))
    lines = story.drama(fn, *args, **kwargs)
    story.presenter = story.represent(lines)
    raise web.HTTPFound("/{0.hex}".format(uid))


async def post_player(request):
    log = logging.getLogger("tos.app.player")
    data = await request.post()
    name = data["name"]
    if not Story.validators["player"].match(name):
        raise web.HTTPUnauthorized(reason="User input invalid name.")

    story = Story()
    story.drama = story.load_drama(player_name=name)
    story.folder = story.load_folder()
    uid = story.drama.player.id
    request.app["stories"][uid] = story
    log.info("Player {0} created story {1!s}".format(name, uid))
    raise web.HTTPFound("/{0.hex}".format(uid))


async def get_titles(request):
    path = importlib.resources.path("tos.web", "titles.html")
    with path as p:
        text = p.read_text().format(Story.render_dict_to_css(Story.definitions))
        return web.Response(text=text, content_type="text/html")


def build_app(args):
    app = web.Application()
    app.add_routes([
        web.get("/", get_titles),
        web.post("/story/", post_player),
        web.post("/{{story:{0}}}/cmd/".format(Story.validators["session"].pattern), post_command),
        web.get("/{{story:{0}}}".format(Story.validators["session"].pattern), get_frame),
    ])
    app.router.add_static(
        "/css/base/",
        pkg_resources.resource_filename("turberfield.catchphrase", "css")
    )
    app.router.add_static(
        "/css/theme/",
        pkg_resources.resource_filename("tos.web", "css")
    )
    app["stories"] = {}
    return app


def main(args):
    app = build_app(args)
    return web.run_app(app, host=args.host, port=args.port)


def parser(description=__doc__):
    rv = argparse.ArgumentParser(description)
    rv.add_argument(
        "--version", action="store_true", default=False,
        help="Print the current version number.")
    rv.add_argument(
        "--host", default="127.0.0.1",
        help="Set an interface on which to serve."
    )
    rv.add_argument(
        "--port", default=8080, type=int,
        help="Set a port on which to serve."
    )
    return rv


def run():
    p = parser()
    args = p.parse_args()

    rv = 0
    if args.version:
        sys.stdout.write(tos.__version__)
        sys.stdout.write("\n")
    else:
        rv = main(args)

    if rv == 2:
        p.print_help()

    sys.exit(rv)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
