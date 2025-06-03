import flet as ft
from models.usuario.session import User_session


class Dashboard:
    def __init__(self, page: ft.Page):
        self.page = page
        self.user = User_session.UserObject

        self.page.title = "Dashboard"
        self.page.padding = 0
        self.page.spacing = 0
        self.page.theme_mode = "light"
        self.page.scroll = "auto"
        page.window.width = 1100
        page.window.height = 650
        page.window.resizable = True

        self.log_view = ft.ListView(height=150, spacing=5, auto_scroll=True)
        self.content_view = ft.Container(expand=True, bgcolor="#F8F9FA")

        self.sidebar = self._build_sidebar()
        self._render_home()

        self.page.add(
            ft.Row(
                controls=[
                    self.sidebar,
                    self.content_view,
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH
            )
        )

    def _build_sidebar(self):
        menu_items = [
            ("🏠 Início", self._render_home),
            ("👤 Perfil", self._render_profile),
            ("⚙️ Configurações", self._render_settings),
            ("🚪 Sair", self._render_logout),
        ]

        self.selected_index = None
        self.sidebar_buttons = []

        def on_button_click(e, index, handler):
            # Marcar item selecionado
            for i, item in enumerate(self.sidebar_buttons):
                item.bgcolor = "black" if i == index else "transparent"
            self.selected_index = index
            self.page.update()
            handler()

        def create_button(index, label, handler):
            container = ft.Container(
                bgcolor="transparent",
                border_radius=10,
                animate=ft.Animation(300, "easeInOut"),
                content=ft.TextButton(
                    text=label,
                    on_click=lambda e: on_button_click(e, index, handler),
                    style=ft.ButtonStyle(
                        padding=ft.Padding(12, 10, 12, 10),
                        color="black",
                        overlay_color="rgba(255,255,255,0.1)",
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
            )

            # Hover usando event handler correto
            def on_hover(e):
                if self.selected_index != index:
                    container.bgcolor = "rgba(255,255,255,0.08)" if e.data == "true" else "transparent"
                    self.page.update()

            container.on_hover = on_hover
            self.sidebar_buttons.append(container)
            return container

        button_controls = [
            create_button(i, label, handler) for i, (label, handler) in enumerate(menu_items)
        ]

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("📁 Painel", size=22, weight="bold", color="white"),
                    ft.Divider(color="rgba(255,255,255,0.2)"),
                    *button_controls,
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=12,
                expand=True
            ),
            bgcolor="rgba(44, 62, 80, 0.95)",
            padding=20,
            width=240,
            height=self.page.height
        )


    def _render_home(self):
        self.content_view.content = ft.Column(
            controls=[
                self._build_header("Início"),
                ft.Container(
                    content=ft.Text("Bem-vindo ao Painel!", size=18),
                    padding=20,
                    bgcolor="#FFFFFF",
                    border_radius=8
                ),
                self._build_logs_area()
            ],
            spacing=20,
            scroll="auto"
        )
        self.page.update()

    def _render_profile(self):
        self.content_view.content = ft.Column(
            controls=[
                self._build_header("Perfil"),
                self._build_profile_card()
            ],
            spacing=20,
            scroll="auto"
        )
        self.page.update()

    def _render_settings(self):
        self.content_view.content = ft.Column(
            controls=[
                self._build_header("Configurações"),
                ft.Container(
                    content=ft.Text("⚙️ Configurações do sistema em breve...", size=16),
                    padding=20,
                    bgcolor="#FFFFFF",
                    border_radius=8
                )
            ],
            spacing=20,
            scroll="auto"
        )
        self.page.update()

    def _render_logout(self):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Logout! Encerrando sessão...", color="white"),
            bgcolor="#E74C3C",
            open=True
        )
        self.page.update()

    def _build_header(self, title: str):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(title, size=24, weight="bold", color="#2D3E50"),
                    ft.Container(expand=True),
                    ft.ElevatedButton(
                        text="🔄 Sincronizar",
                        icon=ft.Icons.CLOUD_SYNC,
                        on_click=self._sync_clicked,
                        style=ft.ButtonStyle(
                            bgcolor="#2980B9",
                            color="white",
                            padding=ft.Padding(10, 10, 0, 0),
                            shape=ft.RoundedRectangleBorder(radius=8),
                            elevation=2,
                        )
                    ),
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
                    ft.Text("📄 Dados do Perfil", size=20, weight="bold", color="#2D3E50"),
                    ft.Divider(),
                    ft.Text(f"👤 Nome: {self.user.nome} {self.user.sobrenome}", size=16),
                    ft.Text(f"🧾 Usuário: @{self.user.username}", size=16),
                    ft.Text(f"📧 E-mail: {self.user.email}", size=16),
                    ft.Text(f"📁 Diretório: {self.user.nome_diretorio}", size=16),
                    ft.Text(f"📅 Criado em: {self.user.data_criacao.strftime('%d/%m/%Y %H:%M:%S')}", size=16),
                ],
                spacing=10
            ),
            padding=20,
            margin=ft.Margin(0, 0, 20, 0),
            bgcolor="#FFFFFF",
            border_radius=10,
            border=ft.border.all(1, "#D1D5DB"),
            shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.with_opacity(0.1, "black")),
        )

    def _build_logs_area(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("📋 Logs e Notificações", size=16, weight="bold", color="#2D3E50"),
                    self.log_view
                ],
                spacing=10
            ),
            padding=20,
            bgcolor="#FFFFFF",
            border_radius=10,
            border=ft.border.all(1, "#D1D5DB"),
            shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.with_opacity(0.08, "black")),
        )

    def _sync_clicked(self, e):
        self._log("Iniciando sincronização com o servidor...")
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Sincronização iniciada!", color="white"),
            bgcolor="#27AE60",
            open=True
        )
        self.page.update()
        self._log("Sincronização concluída com sucesso.")

    def _log(self, msg: str):
        self.log_view.controls.append(ft.Text(f"🔔 {msg}", size=14))
        self.page.update()
