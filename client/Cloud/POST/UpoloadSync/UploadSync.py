
from utils.ServerRoutes.Routes import RoutesServer
import mimetypes
import requests
from log.log import LogRequest


class UploadSync:
    def __init__(self):
        self.uploadSyncRoute = RoutesServer().routeUploadSync

    def __getMimeType__(self, file_path: str) -> str:
        HashFile, _ = mimetypes.guess_type(file_path)
        return HashFile or "application/octet-stream"

    def request(self, file_path, rel_path:str):
        try:
            HashFile = self.__getMimeType__(file_path)
            
            files = {"file": (rel_path,  open(file_path, "rb"), HashFile)}
            data = {"rel_path": rel_path}
            
            response = requests.post(self.uploadSyncRoute, files=files, data=data)
            match response.status_code:
                case 200:
                    return self.__reponse__(response)
                case 400:
                    return self.__reponse__(response)
                case 404:
                    return self.__reponse__(response)
                case 500:
                    return self.__reponse__(response)
                
        except requests.RequestException as e:
            return {'status': False, 'error': str(e), 'message': 'Erro ao tentar subir o arquivo para o servidor.'}
         
        except Exception as ex:
            LogRequest(f"Erro inesperado: {str(ex)}", 'cliente').request_log()
            return {'status': False, 'error': str(ex), 'message': 'Erro inesperado ao tentar subir o arquivo para o servidor.'}

    def __reponse__(self, response: requests.Response):
        data = response.json()
        status = data.get('status')
        error_message = data.get('error')
        mensagem = data.get('message')

        if not status:
            LogRequest(error_message, 'cliente').request_log()
            return {'status': status, 'error': error_message, 'message': mensagem}

        return {'status': status, 'error': '', 'message': mensagem}
            
