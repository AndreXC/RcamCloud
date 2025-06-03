

from WatchdogPath.actions.ActionsResponse.actionsResponse import TratadorResposta
from Cloud.ControllerRoutes import ControllerRoutes
from log.log import LogRequest


class FilesSyncClient:
    def __init__(self):
        self.ResponseHandler = TratadorResposta()
        self.ControllerRoutes=ControllerRoutes()
        self.RouteUploadSync = self.ControllerRoutes.Get.DownloadFiles
        self.RouteDownloadSync = self.ControllerRoutes.Post.UploadSync
        self.SyncArquivos = self.ControllerRoutes.Post.SyncFiles
        
        
    def baixar_arquivo_Client(self, rel_path: str):
        try:
            response:dict = self.ControllerRoutes.Get.DownloadFiles(file=rel_path)
            if response.get('status'):
                destino = self.client_base / rel_path
                destino.parent.mkdir(parents=True, exist_ok=True)
                with open(destino, 'wb') as arq:
                    arq.write(response.content)
                return {'status': True, 'message': f'Arquivo {rel_path} baixado com sucesso.'}
            return {'status': False, 'error': response.get('error'), 'message': response.get('message')}    
        except Exception as e:
            return {'status': False, 'error': str(e), 'message': 'Erro ao tentar baixar o arquivo do servidor.'}
        
        
    def enviar_arquivo_server(self, rel_path: str):
        caminho_local = self.client_base / rel_path
        try:
            if not caminho_local.exists():
                return {'status': False, 'error': 'Arquivo não encontrado.', 'message': f'O arquivo {rel_path} não existe no cliente.'}

            response = self.ControllerRoutes.Post.UploadSync(file_path=caminho_local, rel_path=rel_path)
            if response.get('status'):
                return {'status': True, 'message': f'Arquivo {rel_path} enviado com sucesso.'}
            return {'status': False, 'error': response.get('error'), 'message': response.get('message')}
        except Exception as e:
            return {'status': False, 'error': str(e), 'message': 'Erro ao tentar enviar o arquivo para o servidor.'}

        
    def sincronizar(self):
        try:
            response:dict = self.ControllerRoutes.Post.SyncFiles()
            if not response.get('status'):
                LogRequest(response.get('error'), 'cliente').request_log()
                return {'status': False, 'error': response.get('error'), 'message': response.get('message')}
            
            arquivos_para_baixar = response.get('Arquivos_para_baixar')
            arquivos_para_enviar = response.get('Arquivos_para_enviar')
            
            if arquivos_para_baixar:
                for arquivo in arquivos_para_baixar:
                    response = self.baixar_arquivo_Client(arquivo)
                    self.ResponseHandler.tratar(response,'BaixarArquivo', {'path': arquivo})
    
            if arquivos_para_enviar:        
                for arquivo in arquivos_para_enviar:
                    self.enviar_arquivo_server(arquivo)
                    
            return {'status': True, 'message': 'Sincronização concluída com sucesso.'}
                
            
        except Exception as e:
            return {'status': False, 'error': str(e), 'message': 'Erro ao tentar sincronizar os arquivos.'}
        