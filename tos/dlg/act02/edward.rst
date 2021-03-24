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
   :states: tos.types.Motivation.leader
            tos.mixins.types.Proximity.present

.. entity:: PHONE
   :types:  tos.mixins.types.Artifact
   :states: tos.map.Map.Location.office
            tos.mixins.types.Significance.suppress

.. entity:: STORY
   :types:  tos.story.Story

.. entity:: DRAMA
   :types:  turberfield.catchphrase.drama.Drama

.. entity:: SETTINGS
   :types:  turberfield.catchphrase.render.Settings


.. |SNIPPET| property:: PHONE.messages[0].tags[1]

Lionheart
=========

{0}

Action
------

[EDWARD]_

    Got a message for me?

    Maybe about |SNIPPET|?
