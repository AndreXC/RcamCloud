# import os
# import flet as ft


# TOKEN_PATH = "token.txt"

# def main(page: ft.Page):
#     # 1. Define o tamanho da janela ANTES de centralizar
#     page.window_width = 600
#     page.window_height = 600
#     page.window_resizable = False
#     page.window_maximizable = False
#     page.window_title_bar_hidden = True

#     # 2. Agora centraliza a janela corretamente
#     page.window_center()

#     # 3. Outras configs visuais
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#     page.title = "CloudSync"
#     page.theme_mode = ft.ThemeMode.LIGHT
#     page.bgcolor = "#F2F3F5"

#     # 4. Conteúdo de teste (apenas para visualizar)
#     page.add(
#         ft.Text("Login", size=32, weight="bold", color="#2D3E50")
#     )


#     page.appbar = ft.AppBar(
#     leading_width=0,
#     title=ft.Container(
#         content=ft.Row(
#             controls=[
#                 ft.Icon(ft.icons.CLOUD, color="#2D3E50", size=35),
#                 ft.Text("CloudSync", color="#2D3E50", weight="bold", size=25)
#             ],
#             spacing=8,
#             vertical_alignment=ft.CrossAxisAlignment.CENTER
#         ),
#         padding=ft.padding.only(left=28)
#     ),
#     center_title=False,
#     bgcolor="transparent",
#     elevation=0,
#     actions=[
#         ft.Container(
#             content=ft.IconButton(
#                 icon=ft.icons.CLOSE,
#                 icon_color="#2D3E50",
#                 tooltip="Fechar",
#                 on_click=lambda e: page.window_close()
#             ),
#             margin=ft.margin.only(right=12)
#         )
#     ]
# )




#     def check_token():
#         if os.path.exists(TOKEN_PATH):
#             page.snack_bar = ft.SnackBar(ft.Text("Token encontrado. Redirecionando..."))
#             page.snack_bar.open = True
#             page.update()
#             # abrir a tela principal aqui
#         else:
#             show_login()
            

#     def show_login():
#         user_input = ft.TextField(
#             label="Usuário",
#             border_radius=10,
#             border_color="#C2C2C2",
#             bgcolor="#FFFFFF",
#             width=320
#         )
#         password_input = ft.TextField(
#             label="Senha",
#             password=True,
#             can_reveal_password=True,
#             border_radius=10,
#             border_color="#C2C2C2",
#             bgcolor="#FFFFFF",
#             width=320
#         )

#         def login_clicked(e):
#             username = user_input.value.strip()
#             password = password_input.value.strip()
#             hostname = 'teste'

#             try:
#                 # res = requests.post(f"http://{hostname}/auth", json={
#                 #     "username": username,
#                 #     "password": password
#                 # })

#                 status =200
#                 # if res.status_code == 200 and "token" in res.json():
#                 if status == 200:
#                     show_code_input()
#                     # token = res.json()["token"]
#                     # with open(TOKEN_PATH, "w") as f:
#                     #     f.write(token)
               
#                 else:
#                     page.snack_bar = ft.SnackBar(ft.Text("Usuário ou senha inválidos", color="white"))
#                     page.snack_bar.bgcolor = "#D9534F"
#                     page.snack_bar.open = True
#                     page.update()
#             except Exception as ex:
#                 page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {str(ex)}", color="white"))
#                 page.snack_bar.bgcolor = "#D9534F"
#                 page.snack_bar.open = True
#                 page.update()

#         login_card = ft.Container(
#             width=400,
#             padding=30,
#             border_radius=20,
#             bgcolor="#FFFFFF",
#             content=ft.Column(
#                 [
#                     ft.Text("Bem-vindo ao CloudSync", size=24, weight="bold", color="#2E2E2E"),
#                     ft.Text("Acesse sua conta", size=14, color="#6C6C6C"),
#                     ft.Divider(),
#                     user_input,
#                     password_input,
#                     ft.ElevatedButton(
#                         text="Entrar",
#                         on_click=login_clicked,
#                         width=320,
#                         style=ft.ButtonStyle(
#                             bgcolor="#2D3E50",
#                             color="white",
#                             shape=ft.RoundedRectangleBorder(radius=8),
#                             padding=15
#                         )
#                     )
#                 ],
#                 spacing=20,
#                 horizontal_alignment=ft.CrossAxisAlignment.CENTER
#             )
#         )

#         page.controls.clear()
#         page.controls.append(login_card)
#         page.update()

#     def show_code_input():
   
#         def validate_code(e):
#             code = "".join([box.value for box in code_boxes])
#             if len(code) == 4 and code.isdigit():
#                 print(f"Código inserido: {code}")
#                 # validação do código pode ser feita aqui

#         code_boxes = [
#             ft.TextField(
#                 width=60,
#                 height=60,
#                 max_length=1,
#                 text_align="center",
#                 bgcolor="#F9F9F9",
#                 border_color="#D0D0D0",
#                 border_radius=12,
#                 on_change=validate_code,
#                 text_style=ft.TextStyle(size=15, weight="bold"),
#                 counter=ft.Text(" ")
#             )
#             for _ in range(4)
#         ]



#         page.controls.clear()
#         page.controls.append(
#             ft.Container(
#                 padding=30,
#                 width=400,
#                 bgcolor="#FFFFFF",
#                 border_radius=20,
#                 content=ft.Column(
#                     [
#                         ft.Text("Verificação em duas etapas", size=22, weight="bold", color="#2E2E2E"),
#                         ft.Text("Digite o código de 4 dígitos enviado para seu e-mail", size=13, color="#6C6C6C"),
#                         ft.Row(code_boxes, alignment=ft.MainAxisAlignment.CENTER, spacing=15),
#                         ft.Text("", size=12, color="#A0A0A0", italic=True)
#                     ],
#                     spacing=25,
#                     alignment=ft.MainAxisAlignment.CENTER
#                 )
#             )
#         )
#         page.update()


#     check_token()

# ft.app(target=main)

import os
import flet as ft
from auth.Login.login import Login
from auth.CheckAuthToken.checkAuthToken import checkAuthToken
from models.usuario.session import User_session  

class CloudSyncApp:
    def __init__(self, page: ft.Page):
        self.page = page
        # self.token_path = "token.txt"
        self.thema = ft.ThemeMode.LIGHT
        self.bgColor ="#F2F3F5"

    # self.code_boxes = []
      
        self.configure_window_size_aligment()
        self.Layout()
        self.configure_appbar()
        self.check_token()


    def configure_window_size_aligment(self):
        self.page.window_width = 600
        self.page.window_height = 600
        self.page.window_resizable = False
        self.page.window_maximizable = False
        self.page.window_title_bar_hidden = True
        self.page.window_center()
    
    def Layout(self):
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.title = "CloudSync"
        self.page.theme_mode = self.thema
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
                        ft.Icon(ft.icons.CLOUD, color="#2D3E50", size=35),
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
                        icon=ft.icons.CLOSE,
                        icon_color="#2D3E50",
                        tooltip="Fechar",
                        on_click=lambda e: self.page.window_close()
                    ),
                    margin=ft.margin.only(right=12)
                )
            ]
        )

    def check_token(self):
        instanceCheckAuthToken = checkAuthToken()
        status, mensagem = instanceCheckAuthToken.request_token()     
        if status:
            User = User_session.UserObject
            print(User.email)
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Token encontrado. Redirecionando..."),
                open=True
            )
            self.page.snack_bar.bgcolor = "#5CB85C"
            self.page.update()
            self.page.controls.clear()
            self.page.add(
                ft.Text("Tela Principal", size=32, weight="bold", color="#2D3E50")
            )
        else:
            self.show_login()

    def show_login(self):
        self.page.controls.clear()

        user_input = ft.TextField(
            label="Usuário", border_radius=10, border_color="#C2C2C2",
            bgcolor="#FFFFFF", width=320
        )
        password_input = ft.TextField(
            label="Senha", password=True, can_reveal_password=True,
            border_radius=10, border_color="#C2C2C2", bgcolor="#FFFFFF", width=320
        )

        def login_clicked(e):
            username = user_input.value.strip()
            password = password_input.value.strip()
            
            try:
                # Simulação de sucesso
                instanceLogin = Login(username, password)
                status, message = instanceLogin.authenticate()
            
                
                if status and message == '':
                    self.show_code_input()
                else:
                    self.show_snackbar(message, success=False)
            except Exception as ex:
                self.show_snackbar(f"Erro: {str(ex)}", success=False)

        login_card = ft.Container(
            width=400,
            padding=30,
            border_radius=20,
            bgcolor="#FFFFFF",
            content=ft.Column(
                [
                    ft.Text("Bem-vindo ao CloudSync", size=24, weight="bold", color="#2E2E2E"),
                    ft.Text("Acesse sua conta", size=14, color="#6C6C6C"),
                    ft.Divider(),
                    user_input,
                    password_input,
                    ft.ElevatedButton(
                        text="Entrar",
                        on_click=login_clicked,
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

        self.page.controls.append(login_card)
        self.page.update()

    def show_code_input(self):
        self.page.controls.clear()

        def validate_code(e):
            code = "".join([box.value for box in self.code_boxes])
            if len(code) == 4 and code.isdigit():
                print(f"Código inserido: {code}")
                # Aqui você pode validar o código

        self.code_boxes = [
            ft.TextField(
                width=60, height=60, max_length=1, text_align="center",
                bgcolor="#F9F9F9", border_color="#D0D0D0", border_radius=12,
                on_change=validate_code,
                text_style=ft.TextStyle(size=15, weight="bold"),
                counter=ft.Text(" ")
            )
            for _ in range(4)
        ]

        verification_card = ft.Container(
            padding=30,
            width=400,
            bgcolor="#FFFFFF",
            border_radius=20,
            content=ft.Column(
                [
                    ft.Text("Verificação em duas etapas", size=22, weight="bold", color="#2E2E2E"),
                    ft.Text("Digite o código de 4 dígitos enviado para seu e-mail",
                            size=13, color="#6C6C6C"),
                    ft.Row(self.code_boxes, alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                    ft.Text("", size=12, color="#A0A0A0", italic=True)
                ],
                spacing=25,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

        self.page.controls.append(verification_card)
        self.page.update()

    def show_snackbar(self, message: str, success: bool = True):
        self.page.snack_bar = ft.SnackBar(
            ft.Text(message, color="white"),
            bgcolor="#5CB85C" if success else "#D9534F",
            open=True
        )
        self.page.update()


def main(page: ft.Page):
    CloudSyncApp(page)


if __name__ == "__main__":
    ft.app(target=main)