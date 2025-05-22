import flet as ft

# Simula usuário logado (você substituirá com verificação real depois)
def validar_login(username, senha):
    return username == "admin" and senha == "123"

# --- Tela de login ---
class Login:
    def __init__(self, page: ft.Page, on_login_success):
        self.page = page
        self.on_login_success = on_login_success  # função para ir pro dashboard
        self.build()

    def build(self):
        self.username = ft.TextField(label="Usuário")
        self.password = ft.TextField(label="Senha", password=True)

        btn_login = ft.ElevatedButton(
            "Entrar",
            on_click=self.processar_login
        )

        self.page.controls.clear()
        self.page.add(
            ft.Column(
                [
                    ft.Text("Login", size=30, weight="bold"),
                    self.username,
                    self.password,
                    btn_login,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        )

    def processar_login(self, e):
        user = self.username.value
        senha = self.password.value

        if validar_login(user, senha):
            # Avisa ao app que login foi bem-sucedido
            self.on_login_success()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Usuário ou senha inválido"), open=True)
            self.page.update()

# --- Tela do Dashboard ---
class Dashboard:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.controls.clear()

        self.page.add(
            ft.Column(
                [
                    ft.Text("Bem-vindo ao Dashboard", size=32, weight="bold"),
                    ft.Text("Aqui vai o conteúdo da aplicação..."),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        )

# --- Função principal ---
def main(page: ft.Page):
    page.title = "Sistema"
    page.theme_mode = "light"

    # Função de transição entre login e dashboard
    def entrar_no_dashboard():
        Dashboard(page)

    # Inicializa com a tela de login
    Login(page, entrar_no_dashboard)

ft.app(target=main)
