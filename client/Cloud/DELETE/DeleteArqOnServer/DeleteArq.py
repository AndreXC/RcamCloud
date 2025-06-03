import traceback
from utils.ServerRoutes.Routes import RoutesServer
import requests
from log.log import LogRequest

 
class DeleteArq:
    def __init__(self):
        self.routeDelete = RoutesServer().routeDelete
    def request(self, rel_path):
        try:
            args = {
                "path": rel_path
            }
            response = requests.delete(self.routeDelete, json=args)
            match response.status_code:
                case 200:
                    return self.__response__(response)
                case 500:
                    return self.__response__(response)
        except Exception as e:
            jsonErro = {'error': str(e), 'traceback': traceback.format_exc(), 'method': 'DeleteArq.request.DELETE', 'rel_path': rel_path, 'route': self.routeDelete}
            LogRequest(f'{jsonErro}', 'cliente').request_log()
            return {'status': False, 'error': str(e), 'message': 'Erro ao tentar remover o arquivo do servidor.'}
        
    def __response__(self, response:requests.Response):
        data:dict = response.json()
        status = data.get('status')        
        error_message = data.get('error')
        mensagem = data.get('message')
        return {'status': status, 'error': error_message, 'message': mensagem}
 
 