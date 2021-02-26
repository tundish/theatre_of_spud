.. |VERSION| property:: tos.story.version

:author:    D E Haynes
:made_at:   2021-02-02
:project:   Theatre of Spud
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Mode.playing
            tos.map.Map.Location.foyer

.. entity:: PUZZLE
   :types:  tos.mixins.types.Artifact

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


.. |PLAYER| property:: PLAYER.name
.. |LOCALE| property:: STORY.drama.location
.. |PUZZLE| property:: PUZZLE.names[0]

Entrance
========

{0}

Discover
--------

.. condition:: PUZZLE.state Awareness.ignorant

|PLAYER| stands in |LOCALE|.


Hint
----

.. condition:: STORY.drama.history[0].args[0] hint

I wonder if there's anyone around?

