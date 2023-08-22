from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple, Union
from xml.etree.ElementTree import TreeBuilder
from wikipedia import WikipediaPage, page
from enum import Enum
from pydantic import BaseModel
from bs4 import BeautifulSoup, Tag
from rich import print
class WikiContent(BaseModel):
    page_id: Optional[int]
    original_title: Optional[str]
    url: Optional[str]
    images: Optional[List[str]]
    links: Optional[List[str]]
    references: Optional[List[str]]
    coordinates: Optional[Union[Tuple[Decimal, Decimal], None]]
    summary: Optional[str]
    content: Optional[str]
    html: Optional[str]


class PageReturnables(Enum):
    """
    Enum to let know the dev/user which stuffs can
    be got from the simple api wrapper
    """

    CONTENT = "content"
    COORDINATES = "coordinates"
    HTML = "html"
    IMAGES = "images"
    LINKS = "links"
    REFERENCES = "references"
    SUMMARY = "summary"
    ORIGINAL_TITLE = "original_title"
    URL = "url"
    WHOLE_PAGE = "whole_page"
    PAGE_ID = "page_id"
    ALL = "all"


def _get_page_content(page: WikipediaPage) -> Union[str, None]:
    """Plain text content of the page, excluding images, tables, and other data."""
    return str(page.content)


def _get_page_coordinates(
    page: WikipediaPage,
) -> Union[Tuple[Decimal, Decimal], None]:
    """Tuple of Decimals in the form of (lat, lon) or None"""
    try:
        return page.coordinates
    except KeyError:
        return None


def _get_page_html(page: WikipediaPage) -> Union[str, None]:
    """Get full page HTML."""
    return str(page.html())


def _get_page_images(page: WikipediaPage) -> List[str]:
    """List of URLs of images on the page."""
    return [str(url) for url in page.images]


def _get_page_links_text(page: WikipediaPage) -> List[str]:
    """List of titles of Wikipedia page links on a page."""
    return [str(url) for url in page.links]


def _get_page_references_links(page: WikipediaPage) -> List[str]:
    """
    List of URLs of external links on a page.
    May include external links within page that aren't technically cited
    anywhere.
    """
    return [str(ref) for ref in page.references]


def _get_page_summary(page: WikipediaPage) -> str:
    """Plain text summary of the page."""
    return str(page.summary)


def _get_page_original_title(page: WikipediaPage) -> Union[str, None]:
    """The Page's Title as described on the Wiki Page"""
    return str(page.original_title) or None


def _get_page_url(page: WikipediaPage) -> Union[str, None]:
    """The URL that points to the page on the wikipedia"""
    return str(page.url) or None


def _get_page_id(page: WikipediaPage) -> Union[int, None]:
    """Returns the Unique page id of the page"""
    return int(page.pageid) or None


def _get_all(page: WikipediaPage) -> WikiContent:
    """
    Returns a dictionary of all sorts of returnable stuffs
    """
    return WikiContent(
        page_id=_get_page_id(page),
        original_title=_get_page_original_title(page),
        url=_get_page_url(page),
        links=_get_page_links_text(page),
        images=_get_page_images(page),
        references=_get_page_references_links(page),
        coordinates=_get_page_coordinates(page),
        summary=_get_page_summary(page),
        content=_get_page_content(page),
        html=_get_page_html(page),
    )


def _get_whole_page(
    title: str,
    *,
    pageid: Optional[int] = None,
    auto_suggest: Optional[bool] = False,
    redirect: Optional[bool] = True,
    preload: Optional[bool] = False,
):
    """
    Get a WikipediaPage object for the page with title title or the pageid pageid (mutually exclusive).

    Keyword arguments:

    title - the title of the page to load
    pageid - the numeric pageid of the page to load
    auto_suggest - let Wikipedia find a valid page title for the query
    redirect - allow redirection without raising RedirectError
    preload - load content, summary, images, references, and links
    """
    return page(
        title=title,
        pageid=pageid,
        auto_suggest=auto_suggest,  # type: ignore
        redirect=redirect,  # type: ignore
        preload=preload,  # type: ignore
    )


def get_wiki(
    title: str,
    get_what: PageReturnables = PageReturnables.WHOLE_PAGE,
    *,
    pageid: Optional[int] = None,
    auto_suggest: Optional[bool] = False,
    redirect: Optional[bool] = True,
    preload: Optional[bool] = False,
) -> Union[
    str,
    Tuple[Decimal, Decimal],
    List[str],
    WikipediaPage,
    int,
    Dict[PageReturnables, Any],
    WikiContent,
    None,
]:
    """
    Get content/page from wikipedia
    """
    page_: WikipediaPage = _get_whole_page(
        title=title,
        pageid=pageid,
        auto_suggest=auto_suggest,
        redirect=redirect,
        preload=preload,
    )
    match get_what:
        case PageReturnables.CONTENT:
            return _get_page_content(page_)
        case PageReturnables.COORDINATES:
            return _get_page_coordinates(page_)
        case PageReturnables.HTML:
            return _get_page_html(page_)
        case PageReturnables.IMAGES:
            return _get_page_images(page_)
        case PageReturnables.LINKS:
            return _get_page_links_text(page_)
        case PageReturnables.REFERENCES:
            return _get_page_references_links(page_)
        case PageReturnables.SUMMARY:
            return _get_page_summary(page_)
        case PageReturnables.ORIGINAL_TITLE:
            return _get_page_original_title(page_)
        case PageReturnables.URL:
            return _get_page_url(page_)
        case PageReturnables.WHOLE_PAGE:
            return page_
        case PageReturnables.PAGE_ID:
            return _get_page_id(page_)
        case PageReturnables.ALL:
            return _get_all(page_)
        case _:
            return page_


if __name__ == "__main__":
    links = get_wiki("Python Programming", get_what=PageReturnables.HTML)
    _get_page_link_text_with_url(links)
