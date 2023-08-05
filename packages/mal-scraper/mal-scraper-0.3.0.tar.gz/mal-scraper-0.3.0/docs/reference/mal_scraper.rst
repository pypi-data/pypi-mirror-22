Core API
========

The library supports retrieving Anime, User Profile/Stats, and User-Anime Info.

Anime and Users are identified by `id_ref`s which are integers for anime and
strings for Users, so while you can enumerate through Anime, you must 'discover'
Users.

.. testsetup::

    from mal_scraper import *

.. automodule:: mal_scraper
    :members:
    :imported-members:
    :exclude-members: AgeRating, AiringStatus, ConsumptionStatus, Format,
        Season, ParseError
