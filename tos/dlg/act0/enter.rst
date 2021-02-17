.. |VERSION| property:: tos.story.version

:author:    D E Haynes
:made_at:   2021-02-02
:project:   Theatre of Spud
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tos.types.Character
   :states: tos.types.Motivation.player
            tos.moving.Location.car_park

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: DRAMA
   :types:  turberfield.catchphrase.drama.Drama

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


Entrance
========

Mist
----

.. condition:: STORY.drama.turns 0

The Winter afternoon darkens early.
A cold mist has formed in the last hour of the day.

Here
----

|PLAYER| stands in the Car Park of the Theatre.

Traffic
-------

.. condition:: STORY.drama.turns 0

There isn't much traffic.

Dusk
----

.. condition:: STORY.drama.turns 0
.. condition:: STORY.drama.turns 1
.. condition:: STORY.drama.turns 2

On the other side of the road, about 30 yards away, a couple of young men are sitting on a wall.

Dark
----

.. condition:: STORY.drama.turns 2
.. condition:: STORY.drama.turns 3

Two or three figures walk over from the direction of the Church.
They join the others by the wall.


.. |PLAYER| property:: PLAYER.name

Output
------

