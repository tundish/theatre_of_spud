.. |VERSION| property:: tos.story.version

:author:    D E Haynes
:made_at:   2021-02-02
:project:   Theatre of Spud
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Mode.playing
            tos.map.Map.Location.car_park

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


.. |PLAYER| property:: PLAYER.name
.. |LOCALE| property:: STORY.drama.scenery

Entrance
========

{0}

Mist
----

.. condition:: STORY.drama.turns 0

The Winter afternoon darkens early.
A cold mist has formed in the last hour of the day.

|PLAYER| stands |LOCALE|.

.. property:: STORY.prompt For commands to use, enter 'help'.


Traffic
-------

.. condition:: STORY.drama.turns 1

There isn't much traffic.

|PLAYER| stands |LOCALE|.

Dusk
----

.. condition:: STORY.drama.turns 2

On the other side of the road, about 30 yards away, a couple of young men are sitting on a wall.

|PLAYER| stands |LOCALE|.

More
----

.. condition:: STORY.drama.turns 3

Three figures walk over from the direction of the Church.
They join the others by the wall.

|PLAYER| stands |LOCALE|.

Uncouth
-------

.. condition:: STORY.drama.turns 4
.. condition:: STORY.drama.turns 6

|PLAYER| can hear talking from over the road. Someone hawks and spits.

|PLAYER| stands |LOCALE|.

Smoking
-------

.. condition:: STORY.drama.turns 5
.. condition:: STORY.drama.turns 7
.. condition:: STORY.drama.turns 9

It is quite dark now.

|PLAYER| can make out the glow of cigarettes from the group by the wall.

|PLAYER| stands |LOCALE|.

Hint
----

.. condition:: STORY.drama.history[0].args[0] hint

It's not nice out here. Better get inside.

