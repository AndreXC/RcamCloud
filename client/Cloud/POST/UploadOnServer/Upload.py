import traceback
from utils.ServerRoutes.Routes import RoutesServer
import requests
from log.log import LogRequest
from ..CheckHashRouteOnServer.CheckHash import checkHash


class UploadFiles:
    def __init__(self, ):
        self.routeUpload = RoutesServer().routeUpload
        self.checkHashRoute:checkHash = checkHash()
    
    def request(self, filepath, rel_path):
        try:
            if not filepath:
                return {'status': False, 'error': '', 'message': 'O caminho do arquivo está vazio.'}

            if not rel_path:
                return {'status': False, 'error': '', 'message': 'O caminho relativo do arquivo está vazio.'}
            
            
            dataHash = self.checkHashRoute.Request(filepath, rel_path)
            status = dataHash.get('status')
            if status:
                Amatch= dataHash.get('match') 
                if Amatch:
                    args = {
                        'file': (rel_path, open(filepath, "rb"))
                    }                 
                    response = requests.post(self.routeUpload, files=args)
                    match response.status_code:
                        case 200:
                            return self.__response__(response)
                        case 400:
                            return self.__response__(response)
                        case 500:
                            return self.__response__(response)
                        
            return self.__response__(dataHash)      

        except Exception as e:
            JsonErro = {'error': str(e), 'traceback': traceback.format_exc(), 'method': 'Upload.request.POST', 'filepath': filepath, 'rel_path': rel_path, 'route': self.routeUpload}
            LogRequest(f'{JsonErro}', 'cliente').request_log()
            return {'status': False, 'error': str(e), 'message': 'Erro ao tentar subir o arquivo para o servidor.'}
        
    def __response__(self, response: requests.Response):
        data: dict = response.json()
        status = data.get('status')
        error_message = data.get('error')
        mensagem = data.get('message')

        if not status:
            LogRequest(error_message, 'cliente').request_log()
            return {'status': status, 'error': error_message, 'message': mensagem}
        
        return {'status': status, 'error': '', 'message': mensagem}


