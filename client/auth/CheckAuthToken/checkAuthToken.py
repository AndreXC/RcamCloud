from utils.token.getTokenDisp import GetToken
import requests
from utils.TokenJson.tokenJson import TokenManager
import traceback
from log.log import LogRequest
from models.usuario.usuario import Usuario
from models.usuario.session import User_session  

class checkAuthToken:
    def __init__(self):
        self.routeToken = "https://rcamgeo.com.br/teste2/api/validTokenUser.php"
        self.instanceTokenManager = TokenManager()
    
    def request_token(self):
        token = self.instanceTokenManager.get_token()
        if token == '':
            return False, 'token não encontrado'
        
        payload = {
            'token_dispositivo': GetToken().generate_token(),
            'token': token          
        }
              
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.post(self.routeToken, data=payload, headers=self.headers)
            if response.status_code == 200:
                if response.json().get('token_valido') == True:
                    if 'tokenNovo' in response.json():
                        self.instanceTokenManager.set_token(response.json().get('tokenNovo'))
                    instanceUsuario:Usuario = Usuario
                    User_session.UserObject = instanceUsuario.from_dict(response.json().get('usuario'))
                    return True, ''
                return False, response.json().get('error')
            else:
                error_message= response.json().get('error')
                LogRequest(error_message, 'cliente').request_log()
                return False, error_message
        except requests.RequestException as e:
            error_message = f"{str(e)}\n{traceback.format_exc()}"
            LogRequest(error_message, 'cliente').request_log()
