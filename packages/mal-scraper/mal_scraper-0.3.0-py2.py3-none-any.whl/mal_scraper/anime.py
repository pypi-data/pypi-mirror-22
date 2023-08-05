import itertools
import logging
from datetime import datetime

from bs4 import BeautifulSoup

from .consts import AiringStatus, Format, Retrieved, Season
from .exceptions import MissingTagError, ParseError
from .mal_utils import get_date
from .requester import request_passthrough

logger = logging.getLogger(__name__)

# Future interface?
# def retrieve_iterative(id_refs, concurrency=10, requester='request_limiter'):
#     # id_refs = int or Iterable[int]
#     pass


def get_anime(id_ref=1, requester=request_passthrough):
    """mal_scraper.get_anime(id_ref=1, requester)

    Return the information for a particular show.

    This will raise exceptions unless we properly and fully retrieve and process
    the web-page.

    Args:
        id_ref (int, optional): Internal show identifier.
        requester (requests-like, optional): HTTP request maker
            This allows us to control/limit/mock requests.

    Returns:
        :class:`.Retrieved`: with the attributes `meta` and `data`.

        `data`::

            {
                'name': str,
                'name_english': str,
                'format': mal_scraper.Format,
                'episodes': int, or None when MAL does not know,
                'airing_status': mal_scraper.AiringStatus,
                'airing_started': date,
                'airing_finished': date, or None when MAL does not know,
                'airing_premiere': tuple(Year (int), Season (mal_scraper.Season))
                    or None (for films, OVAs, specials, ONAs and music),
            }

        See also :class:`.Format`, :class:`.AiringStatus`, :class:`.Season`.

    Raises:
        Network and Request Errors: See Requests library.
        .ParseError: Upon processing the web-page including anything that does
            not meet expectations.

    Examples:

        Retrieve the first anime and get the next anime to retrieve::

            next_anime = 1

            try:
                meta, data = mal_scraper.get_anime(next_anime)
            except mal_scraper.ParseError as err:
                logger.error('Investigate page %s with error %d', err.url, err.code)
            except NetworkandRequestErrors:  # Pseudo-code (TODO: These docs)
                pass  # Retry?
            else:
                mycode.save_data(data, when=meta['when'])

            next_anime = meta['id_ref'] + 1
    """
    url = get_url_from_id_ref(id_ref)

    response = requester.get(url)
    response.raise_for_status()  # May raise

    soup = BeautifulSoup(response.content, 'html.parser')
    data = get_anime_from_soup(soup)  # May raise

    meta = {
        'when': datetime.utcnow(),
        'id_ref': id_ref,
        'response': response,
    }

    return Retrieved(meta, data)


def get_url_from_id_ref(id_ref):
    # Use HTTPS to avoid auto-redirect from HTTP (except for tests)
    from .__init__ import FORCE_HTTP
    protocol = 'http' if FORCE_HTTP else 'https'
    return '{}://myanimelist.net/anime/{:d}'.format(protocol, id_ref)


def get_anime_from_soup(soup):
    """Return the anime information from a soup of HTML.

    Args:
        soup (Soup): BeatifulSoup object

    Returns:
        A data dictionary::

            {
                'name': str,
                'name_english': str,
                'format': mal_scraper.Format,
                'episodes': int, or None when MAL does not know,
                'airing_status': mal_scraper.AiringStatus,
                'airing_started': date,
                'airing_finished': date, or None when MAL does not know,
                'airing_premiere': tuple(Year (int), Season (mal_scraper.Season))
                    or None (for films, OVAs, specials, ONAs and music),
            }

    Raises:
        ParseError: If any component of the page could not be processed
            or was unexpected.
    """
    process = [
        ('name', _get_name),
        ('name_english', _get_english_name),
        ('format', _get_format),
        ('episodes', _get_episodes),
        ('airing_status', _get_airing_status),
        ('airing_started', _get_start_date),
        ('airing_finished', _get_end_date),
        ('airing_premiere', _get_airing_premiere),
    ]

    data = {}
    for tag, func in process:
        try:
            result = func(soup, data)
        except ParseError as err:
            logger.debug('Failed to process tag %s', tag)
            err.specify_tag(tag)
            raise

        data[tag] = result

    return data


def _get_name(soup, data=None):
    tag = soup.find('span', itemprop='name')
    if not tag:
        raise MissingTagError('name')

    text = tag.string
    return text


def _get_english_name(soup, data=None):
    pretag = soup.find('span', string='English:')

    # This is not always present (https://myanimelist.net/anime/15)
    if not pretag:
        return ''

    text = pretag.next_sibling.strip()
    return text


def _get_format(soup, data=None):
    pretag = soup.find('span', string='Type:')
    if not pretag:
        raise MissingTagError('type')

    for text in itertools.islice(pretag.next_siblings, 3):
        text = text.string.strip()
        if text:
            break
    else:
        text = None

    format_ = Format.mal_to_enum(text)
    if not format_:  # pragma: no cover
        # Either we missed a format, or MAL changed the webpage
        raise ParseError('Unable to identify format from "{}"'.format(text))

    return format_


def _get_episodes(soup, data=None):
    pretag = soup.find('span', string='Episodes:')
    if not pretag:
        raise MissingTagError('episodes')

    episodes_text = pretag.next_sibling.strip().lower()
    if episodes_text == 'unknown':
        return None

    try:
        episodes_number = int(episodes_text)
    except (ValueError, TypeError):  # pragma: no cover
        # MAL probably changed the webpage
        raise ParseError('Unable to convert text "%s" to int' % episodes_text)

    return episodes_number


def _get_airing_status(soup, data=None):
    pretag = soup.find('span', string='Status:')
    if not pretag:
        raise MissingTagError('status')

    status_text = pretag.next_sibling.strip().lower()
    status = {
        'finished airing': AiringStatus.finished,
        'currently airing': AiringStatus.ongoing,
    }.get(status_text, None)

    if not status:  # pragma: no cover
        # MAL probably changed the website
        raise ParseError('Unable to identify status from "%s"' % status_text)

    return status


def _get_start_date(soup, data=None):
    pretag = soup.find('span', string='Aired:')
    if not pretag:
        raise MissingTagError('aired')

    aired_text = pretag.next_sibling.strip()
    start_text = aired_text.split(' to ')[0]

    try:
        start_date = get_date(start_text)
    except ValueError:  # pragma: no cover
        # MAL probably changed their website
        raise ParseError('Unable to identify date from "%s"' % start_text)

    return start_date


def _get_end_date(soup, data=None):
    pretag = soup.find('span', string='Aired:')
    if not pretag:
        raise MissingTagError('aired')

    aired_text = pretag.next_sibling.strip()
    date_range_text = aired_text.split(' to ')

    # Not all Aired tags have a date range (https://myanimelist.net/anime/5)
    try:
        end_text = date_range_text[1]
    except IndexError:
        return None

    if end_text == '?':
        return None

    try:
        end_date = get_date(end_text)
    except ValueError:  # pragma: no cover
        # MAL probably changed their website
        raise ParseError('Unable to identify date from "%s"' % end_text)

    return end_date


def _get_airing_premiere(soup, data):
    pretag = soup.find('span', string='Premiered:')
    if not pretag:
        # Film: https://myanimelist.net/anime/5
        # OVA: https://myanimelist.net/anime/44
        # ONA: https://myanimelist.net/anime/574
        # TODO: Missing Special, Music links
        if data['format'] in (Format.film, Format.ova, Format.special, Format.ona, Format.music):
            return None
        else:
            raise MissingTagError('premiered')

    season, year = pretag.find_next('a').string.lower().split(' ')

    season = Season.mal_to_enum(season)
    if season is None:
        # MAL probably changed their website
        raise ParseError('Unable to identify season from "%s"' % season)

    try:
        year = int(year)
    except (ValueError, TypeError):  # pragma: no cover
        # MAL probably changed their website
        raise ParseError('Unable to identify year from "%s"' % year)

    return (year, season)
