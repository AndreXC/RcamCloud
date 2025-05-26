from utils.token.getTokenDisp import GetToken
import requests
from utils.TokenJson.tokenJson import TokenManager
import traceback
from log.log import LogRequest
from models.usuario.usuario import Usuario
from models.usuario.session import User_session  
from ..CheckAuthToken.checkAuthToken import checkAuthToken

class checkAuth2f:
    def __init__(self):
        self.routeToken = "https://rcamgeo.com.br/teste2/api/CheckAuth2f.php"
        self.instanceTokenManager = TokenManager()
        self.instanceCheckAuthToken = checkAuthToken()
    
    def request_token(self, codigo2f:str):
        tokenDispositivo:str = GetToken().generate_token()
        payload = {
            'codigo2f': codigo2f,
            'token_dispositivo':tokenDispositivo,
        }
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.post(self.routeToken, data=payload, headers=self.headers)
            match response.status_code:
                case 200:
                    response_json = response.json()
                    if response_json.get('status') == 'sucesso':
                        self.instanceTokenManager.set_token(response_json.get('token'))
                        # CRIANDO A SESSÃO DO USUÁRIO
                        responseAuth =   self.instanceCheckAuthToken.request_token()
                        if responseAuth['status'] is True and responseAuth['error'] == '':
                            return {'status': True, 'error': '', 'message': 'Código 2FA verificado com sucesso.'}
                        return {'status': False, 'error': responseAuth['error'], 'message': responseAuth['message']}
                case 400:
                    error_message = response.json().get('error')
                    parametrosAusentes = response.json().get('parametros')
                    LogRequest(error_message, 'cliente').request_log()
                    return {'status': False, 'error': error_message, 'message': f'Parametros ausentes: {parametrosAusentes}'}
            
                case 401:
                    error_message = response.json().get('error')
                    LogRequest(error_message, 'cliente').request_log()
                    return {'status': False, 'error': response.json().get('error'), 'message': 'codigo 2FA inválido ou não autorizado'}
        
                case 500:
                    error_message = response.json().get('error')
                    LogRequest(error_message, 'cliente').request_log()
                    return {'status': False, 'error': error_message, 'message': 'Erro no servidor interno'}
                
        except requests.RequestException as e:
            error_message = f"{str(e)}\n{traceback.format_exc()}"
            LogRequest(error_message, 'cliente').request_log()
