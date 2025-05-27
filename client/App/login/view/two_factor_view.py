import flet as ft
from auth.CheckAuth2f.CheckAuth2f import checkAuth2f
from ...dashboard.dash import Dashboard
from ...notification.notification import SnackNotification
from log.log import LogRequest
           


def resetar_pagina(page: ft.Page):
    page.controls.clear()
    page.window.title_bar_hidden = False
    page.window.resizable = True
    page.window.always_on_top = False
    page.window.full_screen = False
    

    page.title = ""
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.bgcolor = None
    page.vertical_alignment = None
    page.horizontal_alignment = None
    page.appbar = None
    page.fonts = {}
    page.update()
       

class TwoFactorAuthView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.code_boxes = []
        self.loader = ft.ProgressRing(width=25, height=25, color=ft.Colors.BLUE)
        self.loader.visible = False

    def build(self):
        self.code_boxes = [
            ft.TextField(
                width=60, height=60, max_length=1, text_align="center",
                bgcolor="#F9F9F9", border_color="#D0D0D0", border_radius=12,
                text_style=ft.TextStyle(size=15, weight="bold"),
                counter=ft.Text(" "),
                on_change=self.on_change_code,
                autofocus=(i == 0),
                keyboard_type=ft.KeyboardType.NUMBER
            )
            for i in range(4)
        ]

        self.status_text = ft.Text("", size=12, color="#A0A0A0", italic=True)

        return ft.Container(
            padding=30,
            width=400,
            bgcolor="#FFFFFF",
            border_radius=20,
            content=ft.Column(
                [
                    ft.Text("Verificação em duas etapas", size=22, weight="bold", color="#2E2E2E"),
                    ft.Text("Digite o código de 4 dígitos enviado para seu e-mail", size=13, color="#6C6C6C"),
                    ft.Row(self.code_boxes, alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                    ft.Row([self.loader, self.status_text], alignment=ft.MainAxisAlignment.CENTER),
                ],
                spacing=25,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    def on_change_code(self, e):
        for i, box in enumerate(self.code_boxes):
            if box.value and i < len(self.code_boxes) - 1 and self.code_boxes[i + 1].value == "":
                self.code_boxes[i + 1].focus()
                break

        code = "".join([box.value for box in self.code_boxes])
        if len(code) == 4 and code.isdigit():
            self.lock_inputs(True)
            self.loader.visible = True
            self.status_text.value = "Verificando código..."
            self.page.update()

            instanceCheckAuth2f = checkAuth2f()
            response = instanceCheckAuth2f.request_token(code)

            if response['status']:
                resetar_pagina(self.page)
                Dashboard(page=self.page)
            else:
                if response.get('error'):
                    LogRequest(response.get('error',response.get('error') ), 'client').request_log()
                SnackNotification(self.page, ft.Text(response['message'], color='white'), False)

                self.loader.visible = False
                self.status_text.value = "Código incorreto. Tente novamente."
                self.lock_inputs(False)
                self.clear_inputs()
                self.code_boxes[0].focus()
                self.page.update()

    def lock_inputs(self, locked: bool):
        for box in self.code_boxes:
            box.disabled = locked

    def clear_inputs(self):
        for box in self.code_boxes:
            box.value = ""
