import os
from Cloud.ControllerRoutes import ControllerRoutes
from ActionsResponse.actionsResponse import TratadorResposta
from watchdog.events import FileSystemEvent

class ActionsExecute:
    def __init__(self, caminho_base):
        self.caminho_base = caminho_base
        self.controlador = ControllerRoutes()
        self.tratador = TratadorResposta()

    def _caminho_relativo(self, caminho_completo):
        return os.path.relpath(caminho_completo, self.caminho_base).replace("\\", "/")

    def criar(self, evento: FileSystemEvent):
        caminho = self._caminho_relativo(evento.src_path)
        if evento.is_directory:
            resposta = self.controlador.Post.CreateDirectory(caminho)
            self.tratador.tratar(resposta, 'CriarDiretorio', {'caminho': caminho})
        else:
            resposta = self.controlador.Post.UploadFiles(evento.src_path, caminho)
            self.tratador.tratar(resposta, 'EnviarArquivo', {'origem': evento.src_path, 'caminho': caminho})

    def modificar(self, evento:FileSystemEvent):
        if not evento.is_directory:
            caminho = self._caminho_relativo(evento.src_path)
            resposta = self.controlador.Post.UploadFiles(evento.src_path, caminho)
            self.tratador.tratar(resposta, 'EnviarArquivo', {'origem': evento.src_path, 'caminho': caminho})
     
    def remover(self, evento: FileSystemEvent):
        caminho = self._caminho_relativo(evento.src_path)
        resposta = self.controlador.Delete.DeleteArq(caminho)
        self.tratador.tratar(resposta, 'RemoverArquivo', {'caminho': caminho})


    def mover(self, evento: FileSystemEvent):
        caminho_antigo = self._caminho_relativo(evento.src_path)
        caminho_novo = self._caminho_relativo(evento.dest_path)

        resposta_remover = self.controlador.Delete.DeleteArq(caminho_antigo)
        self.tratador.tratar(resposta_remover, 'RemoverArquivo', {'caminho': caminho_antigo})

        if not evento.is_directory:
            resposta_enviar = self.controlador.Post.UploadFiles(evento.dest_path, caminho_novo)
            self.tratador.tratar(resposta_enviar, 'EnviarArquivo', {'origem': evento.dest_path, 'caminho': caminho_novo})

