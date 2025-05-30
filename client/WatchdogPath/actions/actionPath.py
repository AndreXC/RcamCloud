# from watchdog.events import FileSystemEventHandler
# import os
# from Cloud.ControllerRoutes import ControllerRoutes

# class ActionsDirectory(FileSystemEventHandler):
#     def __init__(self, base_path):
#         self.base_path = base_path
#         self.controllerRoutes = ControllerRoutes()

#     def _relative_path(self, full_path):
#         return os.path.relpath(full_path, self.base_path).replace("\\", "/")

#     #cria o diretório no servidor
#     def on_created(self, event):
#         rel_path = self._relative_path(event.src_path)
#         if event.is_directory:
#             self.controllerRoutes.Post.CreateDirectory(rel_path)
#         else:
#             self.controllerRoutes.Post.UploadFiles(event.src_path, rel_path)

#    # Verifica se o arquivo já existe no servidor e faz o upload se necessário
#     def on_modified(self, event):
#         if not event.is_directory:
#             rel_path = self._relative_path(event.src_path)
#             self.controllerRoutes.Post.UploadFiles(event.src_path, rel_path)

#     # Remove o arquivo do servidor
#     def on_deleted(self, event):
#         rel_path = self._relative_path(event.src_path)
#         self.controllerRoutes.Delete.DeleteArq(rel_path)

#     # Move o arquivo, removendo o antigo e enviando o novo
#     def on_moved(self, event):
#         old_rel = self._relative_path(event.src_path)
#         new_rel = self._relative_path(event.dest_path)
#         self.on_deleted(event)
#         if not event.is_directory:
#             self.controllerRoutes.Post.UploadFiles(event.dest_path, new_rel)
            
            
#     def GetResponse(self, response:dict):
#         if not response['status']:
            
            
    
    
    
        
from watchdog.events import FileSystemEventHandler
import os
from Cloud.ControllerRoutes import ControllerRoutes
from fila_arquivos.filaArquivos import FilaArquivosClient
from datetime import datetime

class ActionsDirectory(FileSystemEventHandler):
    def __init__(self, base_path):
        self.base_path = base_path
        self.controllerRoutes = ControllerRoutes()
        self.fila = FilaArquivosClient()

    def _relative_path(self, full_path):
        return os.path.relpath(full_path, self.base_path).replace("\\", "/")

    def _handle_response(self, response: dict, action: str, args: dict):
        if not response.get('status'):
            self.fila.add(action, args)

    def on_created(self, event):
        rel_path = self._relative_path(event.src_path)
        if event.is_directory:
            res = self.controllerRoutes.Post.CreateDirectory(rel_path)
            self._handle_response(res, 'CreateDirectory', {'path': rel_path})
        else:
            res = self.controllerRoutes.Post.UploadFiles(event.src_path, rel_path)
            self._handle_response(res, 'UploadFiles', {'src_path': event.src_path, 'rel_path': rel_path})

    def on_modified(self, event):
        if not event.is_directory:
            rel_path = self._relative_path(event.src_path)
            res = self.controllerRoutes.Post.UploadFiles(event.src_path, rel_path)
            self._handle_response(res, 'UploadFiles', {'src_path': event.src_path, 'rel_path': rel_path})

    def on_deleted(self, event):
        rel_path = self._relative_path(event.src_path)
        res = self.controllerRoutes.Delete.DeleteArq(rel_path)
        self._handle_response(res, 'DeleteArq', {'path': rel_path})

    def on_moved(self, event):
        old_rel = self._relative_path(event.src_path)
        new_rel = self._relative_path(event.dest_path)

        # Primeiro: deletar o antigo
        del_res = self.controllerRoutes.Delete.DeleteArq(old_rel)
        self._handle_response(del_res, 'DeleteArq', {'path': old_rel})

        # Depois: criar o novo
        if not event.is_directory:
            up_res = self.controllerRoutes.Post.UploadFiles(event.dest_path, new_rel)
            self._handle_response(up_res, 'UploadFiles', {'src_path': event.dest_path, 'rel_path': new_rel})
