import traceback
from utils.ServerRoutes.Routes import RoutesServer
import requests
from log.log import LogRequest

class CreateDirectoryApi:
    def __init__(self):
        self.routeCreatedirectory = RoutesServer().routeCreateDirectory

    def request(self, rel_path):
        try:
            path = {'path': rel_path}
            response = requests.post(self.routeCreatedirectory, json=path)

            match response.status_code:
                case 200:
                    return self.__response__(response)
                case 201:
                    return self.__response__(response)
                case 500:
                    return self.__response__(response)
                
        except Exception as e:
            error_message = f"{str(e)}\n{traceback.format_exc()}"
            LogRequest(error_message, 'cliente').request_log()
            return {'status': False, 'error': error_message, 'message': 'Erro ao tentar subir o arquivo para o servidor.'}
        
        
    def __response__(self, response: requests.Response):
        data: dict = response.json()
        status = data.get('status')
        error_message = data.get('error')
        mensagem = data.get('message')

        if not status:
            LogRequest(error_message, 'cliente').request_log()
            return {'status': status, 'error': error_message, 'message': mensagem}
        
        return {'status': status, 'error': '', 'message': mensagem}
    