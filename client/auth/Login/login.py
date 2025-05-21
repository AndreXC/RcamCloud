from utils.token.getTokenDisp import GetToken
import requests
from utils.TokenJson.tokenJson import TokenManager
from log.log import LogRequest
import traceback
import re

class Login:
    def __init__(self, email:str, password:str):
        self.routeAuth = "https://rcamgeo.com.br/teste2/api/authUser.php"
        self.routeToken = "https://rcamgeo.com.br/teste2/api/validTokenUser.php"
        self.email:str = email
        self.password:str = password
        self.tokeuser:str = str(GetToken().generate_token())
        self.InstanceTokenManager:TokenManager = TokenManager()
    
    def authenticate(self):
        def is_valid_email(email: str) -> bool:
            """
            Valida se o e-mail informado possui um formato válido.
            """
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            return re.match(pattern, email) is not None
        
        if not is_valid_email(self.email):
            return False, 'Formato de e-mail inválido. Por favor, insira um e-mail válido.'
        
        payload = {
            'email': self.email,
            'senha': self.password,
            'tokenDispositivo': self.tokeuser
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.post(self.routeAuth, data=payload, headers=headers)
            match response.status_code:
                case 200:
                    if response.json().get('status') == 'sucesso':
                        token = response.json().get('token')
                        self.InstanceTokenManager.set_token(token)
                        return True, ''
                    else:
                        mensagemRetorno = response.json().get('error')
                        return False, mensagemRetorno
                case 400:
                    error_message = response.json().get('error')
                    return False, error_message
                case 401:
                    messagemRetorno = response.json().get('error')
                    return False, messagemRetorno
                case 500:
                    mensagemErro = response.json().get('error')
                    LogRequest(mensagemErro, 'cliente').request_log()
                    return False, 'Estamos Com problemas no servidor, tente mais tarde. Entre em contato com o suporte.'
                
        except requests.RequestException as e:
           error_message = f"{str(e)}\n{traceback.format_exc()}"
           LogRequest(error_message, 'cliente').request_log()
                
        


