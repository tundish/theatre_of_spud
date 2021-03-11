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

Auditorium
----------

.. condition:: PLAYER.state tos.map.Map.Location.auditorium

The Auditorium has seats for about 150 people in two blocks.

Steps lead up to the rear exit.

The curtains to the stage are drawn closed.

Backstage
---------

.. condition:: PLAYER.state tos.map.Map.Location.backstage

|PLAYER| stands in a long corridor of breeze block, painted white.

There are a couple of dressing rooms here, and a small toilet.

Balcony
-------

.. condition:: PLAYER.state tos.map.Map.Location.balcony

|PLAYER| is standing on the narrow balcony behind the Auditorium.

Through a door is the Lighting Box. Downstairs is the Bar.

Bar
---

.. condition:: PLAYER.state tos.map.Map.Location.bar

|PLAYER| contemplates the Bar.

Car Park
--------

.. condition:: PLAYER.state tos.map.Map.Location.car_park

|PLAYER| is outside in the Car Park. There is an exit on to a lane which meets the main road.

Cloaks
------

.. condition:: PLAYER.state tos.map.Map.Location.cloaks

The Cloakroom is an oddly elongated space with an open counter on to the Foyer.

Corridor
--------

.. condition:: PLAYER.state tos.map.Map.Location.corridor

The Corridor is draughty, and the carpet worn.

It runs the length of the Auditorium and ends in a door to Backstage.

Costume
-------

.. condition:: PLAYER.state tos.map.Map.Location.costume

The Costume Room is chilly, and slightly damp.

Racks of clothing take up some of the space. The rest is given over to lighting equipment and crates of props.

Office
------

.. condition:: PLAYER.state tos.map.Map.Location.office

The Box Office is a tiny room.

Behind |PLAYER| is the door back to the Foyer.
On the left is a split aluminium window facing the Foyer entrance.

There is a desk and a chair, and a rotary telephone fixed to the wall on the right.

There is nothing else here. Everything of value is locked away.
