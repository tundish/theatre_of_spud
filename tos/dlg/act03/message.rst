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

.. entity:: SPUD
   :types:  tos.mixins.types.Character
   :states: tos.types.Motivation.acting

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


Message
=======

{0}

Action
------

[EDWARD]_

    Got a message for me?

Danny
-----

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Danny

[EDWARD]_

    It's Danny, isn't it?

.. property:: SPUD.state tos.mixins.types.Significance.indicate

Mikey
-----

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Mikey

[EDWARD]_

    It's Mikey, isn't it?

.. property:: SPUD.state tos.mixins.types.Significance.indicate

Hayley
------

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Hayley

[EDWARD]_

    It's Hayley, isn't it?

.. property:: SPUD.state tos.mixins.types.Significance.indicate

