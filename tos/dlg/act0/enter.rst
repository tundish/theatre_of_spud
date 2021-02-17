.. |VERSION| property:: tos.story.version

:author:    D E Haynes
:made_at:   2021-02-02
:project:   Theatre of Spud
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tos.types.Character
   :states: tos.types.Motivation.player
            tos.types.Location.car_park

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


Enter
=====

Action
------

Enter.

{0}

Input
-----

|INPUT_TEXT|

.. |INPUT_TEXT| property:: STORY.input
.. |PLAYER| property:: PLAYER.name

