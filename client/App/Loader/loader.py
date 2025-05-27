
import flet as ft

class Loader:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = ft.Colors.WHITE

        self.loading = ft.Container(
            content=ft.Column(
                controls=[
                    ft.ProgressRing(color=ft.Colors.BLUE_500, width=50, height=50),
                    ft.Text("Verificando sessão...", size=16, color=ft.Colors.BLUE_GREY),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )

    def show(self):
        self.page.controls.clear()
        self.page.add(self.loading)
        self.page.update()

    def clear(self):
        self.page.controls.clear()
        self.page.update()