import flet as ft
from  .view.login_view import LoginView
from .view.two_factor_view import TwoFactorAuthView
class LoginApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.bgColor = "#F2F3F5"
        self.configure_window()
        self.configure_appbar()
        self.show_login()

    def configure_window(self):
        self.page.window.width = 600
        self.page.window.height = 600
        self.page.window.resizable = False
        self.page.window.center()
        self.page.window.title_bar_hidden = True

        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.title = "CloudSync"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = self.bgColor
        self.page.fonts = {
            "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap",
            "Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap"
        }

    def configure_appbar(self):
        self.page.appbar = ft.AppBar(
            leading_width=0,
            title=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.CLOUD, color="#2D3E50", size=35),
                        ft.Text("CloudSync", color="#2D3E50", weight="bold", size=25)
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.padding.only(left=28)
            ),
            center_title=False,
            bgcolor="transparent",
            elevation=0,
            actions=[
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color="#2D3E50",
                        tooltip="Fechar",
                        on_click=lambda _: self.page.window.close()
                    ),
                    margin=ft.margin.only(right=12)
                )
            ]
        )

    def show_login(self):
        self.page.controls.clear()
        login_view = LoginView(self.page, self.show_code_input)
        self.page.controls.append(login_view.build())
        self.page.update()

    def show_code_input(self):
        self.page.controls.clear()
        code_view = TwoFactorAuthView(self.page)
        self.page.controls.append(code_view.build())
        self.page.update()
