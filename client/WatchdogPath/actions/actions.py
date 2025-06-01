from watchdog.events import FileSystemEventHandler
from .ActionsExecute.actionsExecute import ActionsExecute

class ActionsDirectory(FileSystemEventHandler):
    def __init__(self, caminho_base):
        self.executor = ActionsExecute(caminho_base)

    def on_created(self, evento):
        self.executor.criar(evento)

    def on_modified(self, evento):
        self.executor.modificar(evento)

    def on_deleted(self, evento):
        self.executor.remover(evento)

    def on_moved(self, evento):
        self.executor.mover(evento)
