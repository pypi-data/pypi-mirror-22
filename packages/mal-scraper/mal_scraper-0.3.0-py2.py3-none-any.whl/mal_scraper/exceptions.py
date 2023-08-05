"""All exceptions are available directly from `mal_scraper.x`"""

import logging

logger = logging.getLogger(__name__)


class MalScraperError(Exception):
    """Parent to all exceptions raised by this library."""


class ParseError(MalScraperError):
    """A component of the HTML could not be parsed/processed.

    The tag is the "component" under consideration to help determine where
    the error comes from.

    Args:
        message (str): Human readable string describing the problem.
        tag (str, optional): Which part of the page does this pertain to.

    Attributes:
        message (str): Human readable string describing the problem.
        tag (str): Which part of the page does this pertain to.
    """

    def __init__(self, message, tag=None):
        super().__init__(message)
        self.message = message
        self.tag = tag or ''

    def specify_tag(self, tag):
        """Specify the tag later."""
        self.tag = tag


# --- Internal Exceptions ---


class MissingTagError(ParseError):
    """The tag is missing from the soup/web-page.

    This is internal, so you should instead catch :class:`.ParseError`.
    """

    def __init__(self, tag=None):
        super().__init__('Missing from soup/web-page', tag)
