from typing import Optional
import flet as ft


class SearchBar(ft.UserControl):
    def __init__(
        self, width: Optional[float] = None, height: Optional[float] = None
    ):
        super().__init__()

        # * Idea:
        # *     To use container and card and textfield

        self.search_icon = ft.icons.SEARCH_SHARP
        self.search_button = ft.IconButton(
            icon=self.search_icon,
        )
        self.search_field = ft.TextField(
            border=ft.InputBorder.UNDERLINE,
            border_color="#73a18a",
            focused_border_color="#693636",
            width=(width - 50 if width is not None else None),
            height=height,
        )
        self.container = ft.Container(
            content=ft.Row(
                controls=[
                    self.search_field,
                    self.search_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=width,
            height=height,
            padding=ft.padding.symmetric(10, 5),
            margin=5,
        )
        self.card = ft.Card(content=self.container, elevation=6)

    def build(self):
        return self.card


def main(page: ft.Page):
    page.title = __file__
    page.add(SearchBar(750))
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
