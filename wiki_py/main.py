from rich.logging import RichHandler
from rich.console import Console
import logging

l = [
    "sqlalchemy.engine",
    "sqlalchemy.orm",
    "sqlalchemy.pool",
    "sqlalchemy.dialect",
    "flet",
    "flet_core",
]
loggers = []
for ll in l:
    l_l = logging.getLogger(ll)
    l_l.setLevel(logging.DEBUG)
    l_l.addHandler(RichHandler(level=l_l.level, rich_tracebacks=True))
    l_l.addHandler(
        RichHandler(
            level=l_l.level,
            rich_tracebacks=True,
            console=Console(
                file=open("wikiPy.log", "a"),
                width=125,
            ),
        )
    )


from pathlib import Path
from wiki_py.core.wiki import searcher
from wiki_py.core.db import _db as db
from wiki_py.core.db.models import WikiSearch
from wiki_py.core.api.funcs import get_contents
from wiki_py.ui.components.search_field import SearchBar
from wiki_py.ui.components.wiki_content_viewer import (
    Summary,
    WikiPage,
    WikiTitle,
)
import flet as ft


class MainPage(ft.UserControl):
    URL = db.URL(
        drivername="sqlite", database=str(Path.home() / "PyWiki" / "wiki.db")
    )

    def __init__(self):
        super().__init__()

        self.db = db.DataBase(
            self.URL, echo=True, hide_parameters=True, echo_pool=True
        )
        self.db.create_file()
        self.db.create_all_tables()

        self.search_bar = SearchBar(720)
        self.search_bar.search_button.on_click = self.on_clicking_search_btn
        self.container = ft.Column(
            controls=[self.search_bar], alignment="center"
        )

    def on_clicking_search_btn(self, e):
        content = get_contents(
            self.db, str(self.search_bar.search_field.value)
        )  # ! Need to handle None
        title = (
            WikiTitle(content.original_title, str(content.url))
            if not content.original_title is None
            else None
        )
        summary = (
            Summary(content.summary)
            if not content.original_title is None
            else None
        )

        if not (title is None and summary is None):
            self.container.controls.append(title)
            self.container.controls.append(summary)
            self.update()

    def build(self):
        return self.container


def main(page: ft.Page):
    page.title = "PyWiki"
    page.add(MainPage())
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
