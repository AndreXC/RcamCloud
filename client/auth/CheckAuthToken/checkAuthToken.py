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
        token:str = self.instanceTokenManager.get_token()
        if token == '':
            return {'status': False, 'error': '', 'message': 'Token não encontrado.'} 
        
        tokenDispositivo:str = GetToken().generate_token()
        payload = {
            'token_dispositivo':tokenDispositivo,
            'token': token          
        }
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            response = requests.post(self.routeToken, data=payload, headers=self.headers)
            match response.status_code:
                case 200:
                    if response.json().get('token_valido') == True:
                        if 'tokenNovo' in response.json():
                            self.instanceTokenManager.set_token(response.json().get('tokenNovo'))
                
                        instanceUsuario:Usuario = Usuario
                        #CRIANDO A SESSÃO DO USUÁRIO   
                        #variavel de sessão do usuário, apos sua instancia, pode ser chamada em qualquer lugar
                        User_session.UserObject = instanceUsuario.from_dict(response.json().get('usuario'))
                        return {'status': True, 'error': '', 'message': 'Token válido'}
                case 400:
                    error_message = response.json().get('error')
                    parametrosAusentes = response.json().get('parametros')
                    LogRequest(error_message, 'cliente').request_log()
                    return {'status': False, 'error': error_message, 'message': f'Parametros ausentes: {parametrosAusentes}'}
            
                case 401:
                    error_message = response.json().get('error')
                    LogRequest(error_message, 'cliente').request_log()
                    return {'status': False, 'error': response.json().get('error'), 'message': 'Token inválido ou não autorizado'}
                
                
                case 403:
                    error_message = response.json().get('error')
                    LogRequest(error_message, 'cliente').request_log()
                    return {'status': False, 'error': error_message, 'message': 'Usuário não encontrado para este token'}
            
                case 500:
                    error_message = response.json().get('error')
                    LogRequest(error_message, 'cliente').request_log()
                    return {'status': False, 'error': error_message, 'message': 'Erro no servidor'}
                
        except requests.RequestException as e:
            error_message = f"{str(e)}\n{traceback.format_exc()}"
            LogRequest(error_message, 'cliente').request_log()
