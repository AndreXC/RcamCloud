import flet as ft

class TwoFactorAuthView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.code_boxes = []

    def build(self):
        self.code_boxes = [
            ft.TextField(
                width=60, height=60, max_length=1, text_align="center",
                bgcolor="#F9F9F9", border_color="#D0D0D0", border_radius=12,
                text_style=ft.TextStyle(size=15, weight="bold"),
                counter=ft.Text(" "),
                on_change=self.validate_code
            )
            for _ in range(4)
        ]

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
                    ft.Text("", size=12, color="#A0A0A0", italic=True)
                ],
                spacing=25,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    def validate_code(self, e):
        code = "".join([box.value for box in self.code_boxes])
        if len(code) == 4 and code.isdigit():
            print(f"Código inserido: {code}")
