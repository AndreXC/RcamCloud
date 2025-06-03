import traceback
import requests
from utils.ServerRoutes.Routes import RoutesServer
from log.log import LogRequest


class DownloadSync:
    def __init__(self):
        self.routeDownload = RoutesServer().routeDownload

    def request(self, file):
        try:
            if not file:
                return {'status': False, 'error': 'Nenhum arquivo especificado para download.', 'message': 'Erro ao tentar baixar o arquivo do servidor.'}
            
            args = {
                "file": file
            }
            
            response = requests.get(self.routeDownload, params=args)
            match response.status_code:
                case 200:
                    return self.__response__(response)
                case 404:
                    return self.__response__(response)
                case 500:
                    return self.__response__(response)

        except Exception as e:
            json_error = {'error': str(e), 'traceback': traceback.format_exc(), 'method': 'DownloadFiles.request.GET', 'file': file, 'route': self.routeDownload}
            LogRequest(f'{json_error}', 'cliente').request_log()
            return {'status': False, 'error': str(e), 'message': 'Erro ao tentar baixar o arquivo do servidor.'}

    def __response__(self, response: requests.Response):
        data: dict = response.json()
        status = data.get('status')
        error_message = data.get('error')
        mensagem = data.get('message')

        if not status:
            LogRequest(error_message, 'cliente').request_log()
            return {'status': status, 'error': error_message, 'message': mensagem}

        return {'status': status, 'error': '', 'message': mensagem}