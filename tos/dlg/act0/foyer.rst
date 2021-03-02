.. |VERSION| property:: tos.story.version

:author:    D E Haynes
:made_at:   2021-02-02
:project:   Theatre of Spud
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Mode.playing
            tos.map.Map.Location.foyer

.. entity:: EDWARD
   :types:  tos.mixins.types.Character
   :states: tos.types.Motivation.leader

.. entity:: PUZZLE
   :types:  tos.mixins.types.Artifact
   :states: tos.map.Map.Location.foyer

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


.. |PLAYER| property:: PLAYER.name
.. |EDWARD| property:: EDWARD.name
.. |LOCALE| property:: STORY.drama.scenery
.. |PUZZLE| property:: PUZZLE.name

Foyer
=====

{0}

.. property:: STORY.prompt ?

Ignorant
--------

.. condition:: PUZZLE.state tos.mixins.types.Awareness.ignorant

The Foyer is carpeted grey and gloomy. Further on is a bar area.
The Box Office and Cloakroom are in darkness. There are doors to a corridor on the left.

.. property:: PUZZLE.state tos.mixins.types.Awareness.familiar

Indicate
--------

.. condition:: PUZZLE.state tos.mixins.types.Awareness.indicate

|PLAYER| stands |LOCALE|.

Sees |PUZZLE|.

.. property:: PUZZLE.state tos.mixins.types.Awareness.discover

Discover
--------

.. condition:: PUZZLE.state tos.mixins.types.Awareness.discover

|PLAYER| stands |LOCALE|.

Sees |PUZZLE|.

Familiar
--------

.. condition:: PUZZLE.state tos.mixins.types.Awareness.familiar

|PLAYER| stands |LOCALE|.

Sees |PUZZLE|.

Approach
--------

.. condition:: EDWARD.state tos.mixins.types.Proximity.inbound

|PLAYER| hears someone coming.

Leaving
-------

.. condition:: EDWARD.state tos.mixins.types.Proximity.outward

|EDWARD| leaves abruptly.

Hint
----

.. condition:: STORY.drama.history[0].args[0] hint

I wonder if there's anyone around?

