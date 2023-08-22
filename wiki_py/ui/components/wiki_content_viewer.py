from typing import Union, List
import flet as ft
import webbrowser


class Summary(ft.UserControl):
    def __init__(self, summary: Union[str, ft.Text, None] = None):
        super().__init__()

        self._summary = summary

        self.content = (
            ft.Text(
                value=str(self._summary),
                overflow=ft.TextOverflow.VISIBLE,
                weight=ft.FontWeight.W_500,
                size=17,
            )
            if not isinstance(self._summary, ft.Text)
            else self._summary
        )

    def build(self):
        return self.content


class Link(ft.UserControl):
    def __init__(self, link_text: Union[str, ft.Text], link_url: str):
        super().__init__()

        self._link_text = link_text
        self._link_url = link_url
        self.hyper_link_text = (
            ft.Text(value=self._link_text, italic=True, color="#304add")
            if isinstance(self._link_text, str)
            else self._link_text
        )
        self._container = ft.Container(
            content=self.hyper_link_text,
            on_click=self.open_link,
            tooltip=f"Click, to open {self._link_url} in web-browser",
            border=ft.Border(bottom=ft.BorderSide(1, color="#304add")),
        )

    def open_link(self, e):
        try:
            webbrowser.open_new_tab(self._link_url)
        except:
            pass  # * log this

    def build(self):
        return self._container


class WikiTitle(ft.UserControl):
    def __init__(self, title: str, url: str):
        super().__init__()
        self.link = Link(
            ft.Text(title, style=ft.TextThemeStyle.HEADLINE_SMALL), url
        )
        self.link._container.bottom = None
        self.link.hyper_link_text.color = "#d132b4"

    def build(self):
        return self.link


class WikiPage(ft.UserControl):
    def __init__(self, title: WikiTitle, summary: Summary):
        super().__init__()
        self.wiki_page = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[title], alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Card(content=summary, elevation=4, margin=10),
                ],
                alignment="center",
                scroll="always",
            )
        )

    def build(self):
        return self.wiki_page


def main(page: ft.Page):
    page.title = __file__
    # page.add(
    #     Summary(ft.Text("Google", style=ft.TextThemeStyle.HEADLINE_MEDIUM))
    # )
    # page.add(Link("Google", "https://www.google.com/"))
    # page.add(WikiTitle("Google", "https://www.google.com/"))
    from wiki_py.core.wiki.searcher import (
        _get_whole_page,
        _get_page_summary,
        _get_page_url,
        _get_page_original_title,
        _get_page_references_links,
    )

    pag = _get_whole_page("Python Programming")
    lnks = [Link(l, l) for l in _get_page_references_links(pag)]

    ttl = WikiTitle(str(_get_page_original_title(pag)), _get_page_url(pag))  # type: ignore
    sumry = Summary(_get_page_summary(pag))

    page.add(
        ft.Column(
            controls=[WikiPage(ttl, sumry)], scroll=ft.ScrollMode.ALWAYS
        )
    )
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
