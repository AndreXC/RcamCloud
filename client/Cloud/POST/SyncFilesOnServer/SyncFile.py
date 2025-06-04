import requests
from utils.DirectorySnapshot.snapshot import DirectorySnapshot
from utils.ServerRoutes.Routes import RoutesServer

class SyncFiles:
    def __init__(self):
        self.routeSyncFiles = RoutesServer().routeSyncFiles
    
    def request(self):
        try:
            snapshot = DirectorySnapshot()._generate_snapshot()
            args = {"snapshot": snapshot}
            response = requests.post(self.routeSyncFiles, json=args)

            match response.status_code:
                case 200:
                    return self.__response__(response)
                case 404:
                    return self.__response__(response)
                case 500:
                    return self.__response__(response)
          
        except requests.exceptions.RequestException as e:
            return {'status': False, 'error': str(e), 'message': 'Erro ao tentar sincronizar o arquivo no servidor.'}
        except Exception as ex:
            return {'status': False, 'error': str(ex), 'message': 'Erro inesperado ao tentar sincronizar o arquivo no servidor.'}
        
        
    def __response__(self, response: requests.Response):
        data: dict = response.json()
        status = data.get('status', False)
        error_message = data.get('error', '')
        mensagem = data.get('message', '')

        if not status:
            return {
                'status': status,
                'error': error_message,
                'message': mensagem
            }

        dados_sincronizacao = data.get('data', {})
        if not dados_sincronizacao:
            return {
                'status': status,
                'error': error_message,
                'message': mensagem,
                'Arquivos_para_baixar': [],
                'Arquivos_para_enviar': []
            }
            
        ausente_no_cliente = dados_sincronizacao.get('ausente_no_cliente', [])
        Hashs_nao_equivalentes = dados_sincronizacao.get('Hashs_nao_equivalentes', [])
        ausente_no_server = dados_sincronizacao.get('ausente_no_server', [])

        Arquivos_para_baixar = ausente_no_cliente + Hashs_nao_equivalentes
        Arquivos_para_enviar = ausente_no_server

        return {
            'status': status,
            'error': error_message,
            'message': mensagem,
            'Arquivos_para_baixar': Arquivos_para_baixar,
            'Arquivos_para_enviar': Arquivos_para_enviar
        }
