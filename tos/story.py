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

from collections.abc import Callable
import functools
import html
import importlib.resources
import re
import urllib.parse

from turberfield.catchphrase.presenter import Presenter
from turberfield.catchphrase.render import Action
from turberfield.catchphrase.render import Parameter
from turberfield.catchphrase.render import Renderer
from turberfield.catchphrase.render import Settings
from turberfield.dialogue.model import SceneScript

# import logging
# logging.basicConfig(level=logging.DEBUG)

import tos
from tos.map import Map
from tos.mixins.directing import Directing
from tos.mixins.helpful import Helpful
from tos.mixins.moving import Moving
from tos.mixins.types import Character
from tos.mixins.types import Mode

version = tos.__version__


class Story(Renderer):
    """
    Some methods of this class are likely to end up in a later
    version of the Catchphrase library.

    You should keep a regular eye on https://github.com/tundish/turberfield-catchphrase
    to spot new releases.

    """

    definitions = {
        "catchphrase-colour-washout": "hsl(50, 0%, 100%, 1.0)",
        "catchphrase-colour-shadows": "hsl(202.86, 100%, 4.12%)",
        "catchphrase-colour-midtone": "hsl(203.39, 96.72%, 11.96%)",
        "catchphrase-colour-hilight": "hsl(203.06, 97.3%, 56.47%)",
        "catchphrase-colour-glamour": "hsl(353.33, 96.92%, 12.75%)",
        "catchphrase-colour-gravity": "hsl(293.33, 96.92%, 12.75%)",
        "catchphrase-reveal-extends": "both",
    }

    validators = {
        "command": re.compile("[\\w]{1,36}"),
        "session": re.compile("[0-9a-f]{32}"),
        "player": re.compile("[A-Za-z]{2,24}")
    }

    class Act1(Directing, Moving, Helpful): pass

    @staticmethod
    def render_action_form(action: Action, autofocus=False):
        import textwrap
        url = urllib.parse.quote(action.typ.format(*action.ref))
        if action.parameters:
            yield f'<form role="form" action="{url}" method="{action.method}" name="{action.name}">'
            yield "<fieldset>"

        for p in action.parameters:
            typ = "hidden" if p.required == "hidden" else "text"
            if not p.tip.endswith("."):
                yield f'<label for="input-{p.name}-{typ}" id="input-{p.name}-{typ}-tip">{html.escape(p.tip)}</label>'
            if not p.values:
                yield textwrap.dedent(f"""
                    <input
                    name="{p.name}"
                    pattern="{p.regex.pattern if p.regex else ''}"
                    {'required="required"' if p.required else ''}
                    {'autofocus="autofocus"' if autofocus else ''}
                    type="{'hidden' if p.required == 'hidden' else 'text'}"
                    title="{p.tip}"
                    />""")
            elif len(p.values) == 1:
                yield textwrap.dedent(f"""
                    <input
                    name="{p.name}"
                    placeholder="{p.values[0]}"
                    pattern="{p.regex.pattern if p.regex else ''}"
                    {'required="required"' if p.required else ''}
                    {'autofocus="autofocus"' if autofocus else ''}
                    type="{'hidden' if p.required == 'hidden' else 'text'}"
                    title="{html.escape(p.tip)}"
                    />""")
            else:
                yield f'<select name="{p.name}">'
                for v in p.values:
                    yield f'<option value="{v}">{v}</option>'
                yield "</select>"

        yield f'<button type="submit">{action.prompt}</button>'

        if action.parameters:
            yield "</fieldset>"
            yield "</form>"


    @staticmethod
    def render_animated_frame_to_html(frame, controls):
        from turberfield.dialogue.model import Model
        dialogue = "\n".join(Renderer.animated_line_to_html(i) for i in frame[Model.Line])
        stills = "\n".join(Renderer.animated_still_to_html(i) for i in frame[Model.Still])
        audio = "\n".join(Renderer.animated_audio_to_html(i) for i in frame[Model.Audio])
        last = frame[Model.Line][-1] if frame[Model.Line] else Presenter.Animation(0, 0, None)
        controls = "\n".join(Renderer.animate_controls(*controls, delay=last.delay + last.duration, dwell=0.3))
        return f"""
{audio}
<aside class="catchphrase-reveal">
{stills}
</aside>
<main class="catchphrase-reveal">
<ul>
{dialogue}
</ul>
</main>
<nav class="catchphrase-reveal">
<ul>
{controls}
</ul>
</nav>"""


    @staticmethod
    @functools.lru_cache()
    def render_body_html(title="", refresh=None, next_="", base_style="/css/base/catchphrase.css"):
        base_link = '<link rel="stylesheet" href="{0}" />'.format(base_style) if base_style else ""
        heading = " ".join("<span>{0}</span>".format(i.capitalize()) for i in title.split(" "))
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{'<meta http-equiv="refresh" content="{0};{1}">'.format(refresh, next_) if refresh and next_ else ''}
<meta http-equiv="X-UA-Compatible" content="ie=edge">
<title>{title}</title>
{base_link}
{{0}}
</head>
<body>
<style type="text/css">
{{1}}
</style>
<section class="catchphrase-banner">
<h1>{heading}</h1>
</section>
{{2}}
</body>
</html>"""

    def __init__(self, cfg=None, **kwargs):
        self.acts = [self.Act1]
        self.settings = Settings(**self.definitions)
        self.drama = None
        self.folder = None
        self.input = ""
        self.prompt = "?"
        self.metadata = {}

    @property
    def actions(self):
        yield Action(
            "cmd", None, "/{0.id.hex}", [self.drama.player], "post",
            [Parameter("cmd", True, self.validators["command"], [self.prompt], ">")],
            "Enter"
        )

    def load_drama(self, act=0, player_name="", ensemble=None):
        ensemble = ensemble or []
        drama = self.acts[act](Map())

        for obj in ensemble:
            drama.add(obj)

        if player_name:
            for obj in drama.build():
                drama.add(obj)
            drama.add(Character(names=[player_name]).set_state(Mode.playing, Map.Location.car_park))

        drama.player = drama.ensemble[-1]
        return drama

    def load_folder(self, act=0):
        pkg = f"tos.dlg.act{act}"
        path = importlib.resources.files(pkg)
        return SceneScript.Folder(
            pkg=pkg,
            description="Theatre of Spud",
            metadata={},
            paths=[i.name for i in path.glob("*.rst")],
            interludes=None
        )

    def refresh_target(self, url):
        refresh_state = getattr(self.settings, "catchphrase-states-refresh", "inherit").lower()
        if refresh_state == "none":
            return None
        elif refresh_state == "inherit":
            return url
        else:
            return refresh_state

    def represent(self, lines=[], index=None, loop=None):
        #if all(self.metadata.values()):
        #    act = self.metadata.get("act", 0)
        #    self.drama = self.load(act)
        #    self.metadata["act"] = act + 1

        self.metadata.update(self.drama.interlude(self.folder, index, loop=loop))
        # if "act" in metadata

        n, presenter = Presenter.build_presenter(
            self.folder, *lines,
            ensemble=self.drama.ensemble + [self, self.drama, self.settings],
            shot="Drama output"
        )
        if presenter and not(presenter.dwell or presenter.pause):
            setattr(self.settings, "catchphrase-reveal-extends", "none")
            setattr(self.settings, "catchphrase-states-scrolls", "scroll")
        else:
            setattr(self.settings, "catchphrase-reveal-extends", "both")
            setattr(self.settings, "catchphrase-states-scrolls", "visible")

        return presenter
