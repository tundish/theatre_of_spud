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

Entrance
========

{0}

Mist
----

.. condition:: STORY.drama.turns 0

A Winter afternoon.

It is darkening early.
A cold mist has formed in the last hour of day.

|PLAYER| is crossing the road from the High Street.
To the right, about 30 yards away, a couple of young men are sitting on a wall.

Suddenly a car appears.

.. property:: STORY.prompt Enter 'wait' to allow the car to pass.

Traffic
-------

.. condition:: STORY.drama.turns 1

The car speeds off, leaving billows of vapour to settle below street lights.

.. property:: STORY.prompt You can shorten 'wait' to 'w'. Try that now.

More
----

.. condition:: STORY.drama.turns 2

There is a shout. Someone's name.
Three more figures walk over from the direction of the Croft.

.. property:: STORY.prompt Enter 'help' for useful commands.

Banter
------

.. condition:: STORY.drama.turns 3

|PLAYER| can hear cursing and youthful banter.

Nasty
-----

.. condition:: STORY.drama.turns 4

Over by the wall, someone hawks and spits.

Smoking
-------

.. condition:: STORY.drama.turns 5

It is quite dark now.

|PLAYER| can make out the glow of cigarettes from the group by the wall.

Hint
----

.. condition:: STORY.drama.history[0].args[0] hint

It's not nice out here. Better get inside.

