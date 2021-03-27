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

.. |EDWARD| property:: EDWARD.name
.. |PLAYER| property:: PLAYER.name


Message
=======

{0}

Danny
-----

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Danny

[EDWARD]_

    |PLAYER|, was that the telephone ringing earlier?

[PLAYER]_

    It's Danny.

.. property:: SPUD.state tos.mixins.types.Significance.indicate

Mikey
-----

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Mikey

[EDWARD]_

    Ah, |PLAYER|, what now?

[PLAYER]_

    It's Mikey.

[EDWARD]_

    Spud.

[PLAYER]_

    It's a lot to ask. Spud is quite shy.

[EDWARD]_

    But, as 'tis, we cannot miss him.
    He serves in offices that profit us.

.. property:: SPUD.state tos.mixins.types.Significance.indicate

Hayley
------

.. condition:: STORY.bookmark.drama.messengers[0].messages[0].tags[1] Hayley

[EDWARD]_

    Ah, |PLAYER|, what now?

[PLAYER]_

    It's Hayley.

[EDWARD]_

    Spud.

[PLAYER]_

    Are you sure this will work?.

[EDWARD]_

    It will have to work.

    *Aside*

    These three have robbed me.

    And this demi-devil; for he's a bastard one,
    has plotted with them to take my life.

.. property:: SPUD.state tos.mixins.types.Significance.indicate

