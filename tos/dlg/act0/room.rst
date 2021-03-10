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

Bar
---

.. condition:: PLAYER.state tos.map.Map.Location.bar

|PLAYER| contemplates the Bar.

Office
------

.. condition:: PLAYER.state tos.map.Map.Location.office

The Box Office is a tiny room.

Behind |PLAYER| is the door back to the Foyer.
On the left is a split aluminium window facing the Foyer entrance.

There is a desk and a chair, and a rotary telephone fixed to the wall on the right.

There is nothing else here. Everything of value is locked away.
