import traceback
from utils.ServerRoutes.Routes import RoutesServer
import requests
from log.log import LogRequest


class DownloadAllFiles:
    def __init__(self):
        self.routeDownloadAllFiles = RoutesServer().DownloadAllArq
    def request(self):
        try:
            response = requests.get(self.routeDownloadAllFiles)
            match response.status_code:
                case 200:
                    return self.__response__(response)
                case 404:
                    return self.__response__(response)
                case 500:
                    return self.__response__(response)

        except Exception as e:
            json_error = {'error': str(e), 'traceback': traceback.format_exc(), 'method': 'DownloadAllFiles.request.GET',  'route': self.routeDownloadAllFiles}
            LogRequest(f'{json_error}', 'cliente').request_log()
            return {'status': False, 'error': str(e), 'message': 'Erro ao tentar baixar os arquivos do servidor.'}
        
    def __response__(self, response: requests.Response):
        data: dict = response.json()
        status = data.get('status')
        error_message = data.get('error')
        mensagem = data.get('message')

        if not status:
            LogRequest(error_message, 'cliente').request_log()
            return {'status': status, 'error': error_message, 'message': mensagem}

        files = data.get('files')
        return {'status': status, 'error': '', 'message': mensagem, 'files': files}
        