
import flet as ft
from models.usuario.session import User_session  


class Dashboard:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.controls.clear()
        self.user = User_session.UserObject
        self.page.title = "Dashboard - Perfil do Usuário"
        self.page.padding = 0
        self.page.spacing = 0
        self.page.theme_mode = "light"
        self.page.scroll = "auto"

        self.sidebar = self._build_sidebar()
        self.content = self._build_content()

        self.page.add(
            ft.Row(
                controls=[
                    self.sidebar,
                    ft.Container(
                        content=self.content,
                        expand=True,
                        bgcolor="#F9FAFB"
                    ),
                ],
                expand=True
            )
        )

    def _build_sidebar(self):
        menu_items = [
            ("🏠 Início", self._menu_home_clicked),
            ("👤 Perfil", self._menu_profile_clicked),
            ("⚙️ Configurações", self._menu_settings_clicked),
            ("🚪 Sair", self._menu_logout_clicked),
        ]

        buttons = []
        for label, handler in menu_items:
            buttons.append(
                ft.Container(
                    content=ft.TextButton(
                        text=label,
                        on_click=handler,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(12, 12, 12, 12),
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                            overlay_color="#3D566E"
                        )
                    ),
                    padding=ft.Padding(0,0,5, 2),
                    width=180,
                )
            )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Menu", size=18, weight="bold", color="white"),
                    ft.Divider(color="#3A4C5C"),
                    *buttons
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=10
            ),
            bgcolor="#2C3E50",
            padding=20,
            width=200,
        )

    def _build_content(self):
        return ft.Column(
            controls=[
                self._build_header(),
                self._build_profile_card(),
            ],
            expand=True,
            scroll="auto",
            spacing=20
        )

    def _build_header(self):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(f"Olá, {self.user.nome}!", size=24, weight="bold", color="#2D3E50"),
                    ft.Container(expand=True),
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=32, color="#2D3E50"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=20,
            bgcolor="#FFFFFF",
            border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0")),
        )

    def _build_profile_card(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Dados do Perfil", size=22, weight="bold", color="#2D3E50"),
                    ft.Divider(),
                    ft.Text(f"👤 Nome completo: {self.user.nome} {self.user.sobrenome}", size=16),
                    ft.Text(f"🧾 Usuário: @{self.user.username}", size=16),
                    ft.Text(f"📧 E-mail: {self.user.email}", size=16),
                    ft.Text(f"📁 Diretório: {self.user.nome_diretorio}", size=16),
                    ft.Text(f"📅 Criado em: {self.user.data_criacao.strftime('%d/%m/%Y %H:%M:%S')}", size=16),
                ],
                spacing=10
            ),
            padding=20,
            margin=20,
            bgcolor="#FFFFFF",
            border_radius=10,
            border=ft.border.all(1, "#D1D5DB"),
        )

    def _menu_home_clicked(self, e):
        self._alert("Você clicou em Início!")

    def _menu_profile_clicked(self, e):
        self._alert("Você está na página de Perfil!")

    def _menu_settings_clicked(self, e):
        self._alert("Você clicou em Configurações!")

    def _menu_logout_clicked(self, e):
        self._alert("Logout! Encerrar sessão...")

    def _alert(self, msg):
        self.page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="#5CB85C", open=True)
        self.page.update()
