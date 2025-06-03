
import requests
from utils.CalcHash.calcHash import FileHasher
import traceback
from log.log import LogRequest
from utils.ServerRoutes.Routes import RoutesServer


class checkHash:
    def __init__(self):
        self.routeCheckHash = RoutesServer().routeCheckHash

    def request(self, filepath, rel_path):
        try:
            file_hash, mensage = FileHasher.hash_file(filepath)
            if file_hash is None:
                LogRequest(mensage, 'cliente').request_log()
                return {'status': False, 'error': mensage, 'message': 'Erro ao calcular hash do arquivo.'}
            
            args = {
                "filename": rel_path,
                "sha256": file_hash
            }
            
            response = requests.post(self.routeCheckHash, json=args)
            match response.status_code:
                case 200:
                    return self.__response__(response)
                case 400:
                    return self.__response__(response)
                case 404:
                    return self.__response__(response)
                case 500:
                    return self.__response__(response)
                
        except requests.exceptions.RequestException as e:
            error_message = f"{str(e)}\n{traceback.format_exc()}"
            LogRequest(error_message, 'cliente').request_log()
            return {'status': False, 'error': error_message, 'message': 'Erro ao tentar verificar hash no servidor.'}
        
        
    def __response__(self, response:requests.Response):
        data:dict = response.json()
        status = data.get('status')
        error_message = data.get('error')
        mensagem = data.get('message')
        vmatch = data.get('match', None)

        if vmatch is None:
            LogRequest(error_message, 'cliente').request_log()
            return {'status': status, 'error': error_message, 'message': mensagem, 'match': None}
        return {'status': status, 'error': error_message, 'message': mensagem, 'match': vmatch}

