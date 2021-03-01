.. |VERSION| property:: tos.story.version

:author:    D E Haynes
:made_at:   2021-02-03
:project:   Theatre of Spud
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Mode.playing

.. entity:: EDWARD
   :types:  tos.mixins.types.Character
   :states: tos.types.Motivation.leader
            tos.mixins.types.Proximity.present

.. entity:: PUZZLE
   :types:  tos.mixins.types.Artifact
   :states: tos.map.Map.Location.foyer

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings

.. |EDWARD| property:: EDWARD.name
.. |PLAYER| property:: PLAYER.name

Threats
=======

Ignorant
--------

.. condition:: EDWARD.state tos.mixins.types.Awareness.ignorant

|EDWARD| is here.

He is a tall man with grey hair swept back in an elaborate quiff.
He contemplates |PLAYER| with narrowed eyes

.. property:: EDWARD.state tos.mixins.types.Awareness.familiar

Lights
------

.. condition:: PUZZLE.state tos.mixins.types.Awareness.ignorant

[EDWARD]_

    Good evening |PLAYER|, are you well?

[PLAYER]_

    Hello, Edward, yes. A bit nervous.

[EDWARD]_

    First night. A trial, and lets hope, a triumph!

    That mob of hoodlums is hanging around outside.

|EDWARD|'s eyebrows arch dramatically. The light of a green exit sign catches the side of his ruddy, aquiline nose.
