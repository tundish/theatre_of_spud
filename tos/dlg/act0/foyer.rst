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
   :states: tos.map.Map.Location.foyer

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


.. |PLAYER| property:: PLAYER.name
.. |LOCALE| property:: STORY.drama.scenery
.. |PUZZLE| property:: PUZZLE.name

Entrance
========

{0}

Ignorant
--------

.. condition:: PUZZLE.state Awareness.ignorant

|PLAYER| stands |LOCALE|.

It's empty and quiet.

Indicate
--------

.. condition:: PUZZLE.state Awareness.indicate

|PLAYER| stands |LOCALE|.

Sees |PUZZLE|.

.. property:: PUZZLE.state Awareness.discover

Discover
--------

.. condition:: PUZZLE.state Awareness.discover

|PLAYER| stands |LOCALE|.

Sees |PUZZLE|.

Familiar
--------

.. condition:: PUZZLE.state Awareness.familiar

|PLAYER| stands |LOCALE|.

Sees |PUZZLE|.

Hint
----

.. condition:: STORY.drama.history[0].args[0] hint

I wonder if there's anyone around?

