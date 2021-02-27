.. |VERSION| property:: tos.story.version

:author:    D E Haynes
:made_at:   2021-02-27
:project:   Theatre of Spud
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Mode.playing

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


.. |PLAYER| property:: PLAYER.name
.. |LOCALE| property:: STORY.drama.location

In a room
=========

{0}

Info
----

.. condition:: PLAYER.state tos.mixins.types.Motion.routed

|PLAYER| leaves towards the |LOCALE|.

.. property:: STORY.prompt ?
