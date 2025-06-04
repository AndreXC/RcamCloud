# import requests
# import datetime
# import os

# class LogRequest:
#     """
#     Classe responsável por enviar logs de erro para a API remota.
#     """
#     def __init__(self, mensagem_erro: str, tipo: str):
#         self.url_api = "https://rcamgeo.com.br/teste2/api/logs/log.php"
#         self.mensagem_erro = mensagem_erro
#         self.tipo = tipo

#     def request_log(self):
#         """
#         Envia o log de erro para a API. Em caso de falha, registra localmente.
#         """
#         payload = {
#             "erro_message": self.mensagem_erro,
#             "client_id": TokenManager().get_token(),
#             "tipo": self.tipo
#         }

#         headers = {
#             "Content-Type": "application/json",
#             # "Authorization": "Bearer SEU_TOKEN_SEGURO_AQUI"
#         }

#         try:
#             response = requests.post(self.url_api, json=payload, headers=headers, timeout=10)
#             response.raise_for_status()
#         except requests.exceptions.RequestException as e:
#                 LogErroArq(self.mensagem_erro, self.tipo, str(e)).logar_erro()


# class LogErroArq:
#     """
#     Classe responsável por registrar erros localmente em um arquivo de log.
#     """
#     def __init__(self, mensagem_erro: str, tipo:str, erro: str = None):
#         self.mensagem_erro = mensagem_erro
#         self.erro = erro
#         self.tipo = tipo
#         self.data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         self.appdata_dir = os.getenv('APPDATA') or os.path.expanduser("~/.config")
#         self.folder_name = 'RcamCloud'
#         self.file_name = 'logErro.txt'
#         self.file_dir = os.path.join(self.appdata_dir, self.folder_name)
#         self.file_path = os.path.join(self.file_dir, self.file_name)
#         os.makedirs(self.file_dir, exist_ok=True)

#     def logar_erro(self):
#         """
#         Registra a mensagem de erro no arquivo de log.
#         """
#         token = TokenManager().get_token()
#         with open(self.file_path, "a", encoding="utf-8") as log_file:
#             if self.erro != None:
#                 log_file.write(f"{self.tipo} - {self.data_atual} - {self.mensagem_erro} - {self.erro}\n")
#             log_file.write(f"{self.tipo} - {self.data_atual} - {self.mensagem_erro} - cliente: {token}\n")
            
            
