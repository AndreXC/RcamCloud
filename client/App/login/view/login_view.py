import flet as ft
from auth.Login.login import Login
from ...notification.notification import SnackNotification
from  log.log import LogRequest

class LoginView:
    def __init__(self, page: ft.Page, on_success):
        self.page = page
        self.on_success = on_success
        self.user_input = ft.TextField(
            label="Usuário", border_radius=10, border_color="#C2C2C2",
            bgcolor="#FFFFFF", width=320
        )
        self.password_input = ft.TextField(
            label="Senha", password=True, can_reveal_password=True,
            border_radius=10, border_color="#C2C2C2", bgcolor="#FFFFFF", width=320
        )

    def build(self):
        return ft.Container(
            width=400,
            padding=30,
            border_radius=20,
            bgcolor="#FFFFFF",
            content=ft.Column(
                [
                    ft.Text("Bem-vindo ao CloudSync", size=24, weight="bold", color="#2E2E2E"),
                    ft.Text("Acesse sua conta", size=14, color="#6C6C6C"),
                    ft.Divider(),
                    self.user_input,
                    self.password_input,
                    ft.ElevatedButton(
                        text="Entrar",
                        on_click=self.login_clicked,
                        width=320,
                        style=ft.ButtonStyle(
                            bgcolor="#2D3E50", color="white",
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=15
                        )
                    )
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def login_clicked(self, e):
        username = self.user_input.value.strip()
        password = self.password_input.value.strip()
        errors = []
        if not username:
            errors.append("Email")
        if not password:
            errors.append("Senha")

        if errors:
            mensagem = f"Preencha o campo {errors[0]}"
            SnackNotification(self.page, ft.Text(mensagem, color='white'), False)
            self.page.update()
            return
        
        try:
            instanceLogin = Login(username, password)
            response = instanceLogin.authenticate()
            if response['status']:
                self.on_success()
            else:
                if response['error']:
                    LogRequest(response['error'], 'cliente').request_log()
                SnackNotification(self.page, ft.Text(response['message'], color='white'), False)                
                self.page.update()
        except Exception as ex:
            SnackNotification(self.page, ft.Text(ex, color='white'), False)
            self.page.update()
