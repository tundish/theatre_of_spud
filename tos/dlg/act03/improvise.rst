.. |VERSION| property:: tos.story.version

:author:    D E Haynes
:made_at:   2021-02-02
:project:   Theatre of Spud
:version:   |VERSION|

.. entity:: PLAYER
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Mode.playing

.. entity:: EDWARD
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Proximity.present
            tos.types.Motivation.leader

.. entity:: SPUD
   :types:  tos.mixins.types.Character
   :states: tos.mixins.types.Proximity.present
            tos.types.Motivation.acting

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


Improvise
=========

Mikey
-----

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Mikey

[EDWARD]_

    I'll pity thee. Take pains to make thee speak.
    Teach thee each hour one thing or other.


Hayley
------

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Hayley

[EDWARD]_

    What, ho! Slave. Caliban!
    Thou earth, thou. Speak!


King Lear
---------

[EDWARD]_

    Through tattered clothes great vices do appear; Robes and furred gowns hide all.

