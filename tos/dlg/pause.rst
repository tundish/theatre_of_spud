.. |VERSION| property:: tas.story.version

:author:    D E Haynes
:made_at:   2021-02-06
:project:   Theatre of Spud
:version:   |VERSION|
:dwell:     0
:pause:     0

.. entity:: PLAYER
   :types:  tos.stage.Character
   :states: tos.stage.Motivation.player

.. entity:: NPC
   :types:  tos.stage.Character
   :states: tos.stage.Motivation.paused

.. entity:: DRAMA
   :types:  tos.stage.Stage

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


Paused
======

{0}

.. property:: DRAMA.prompt ?
.. property:: NPC.state tos.stage.Motivation.acting
.. property:: SETTINGS.catchphrase-colour-gravity hsl(209.33, 96.92%, 12.75%)
