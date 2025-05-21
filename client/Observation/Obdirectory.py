
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
from RoutesCloud.routes import routes

class ActionsDirectory(FileSystemEventHandler):
    def __init__(self, base_path):
        self.base_path = base_path
        self.routes = routes()

    def _relative_path(self, full_path):
        return os.path.relpath(full_path, self.base_path).replace("\\", "/")

    def on_created(self, event):
        rel_path = self._relative_path(event.src_path)
        if event.is_directory:
            print(f"[DIRETÓRIO CRIADO] {rel_path}")
            self.routes._create_directory_on_server(rel_path)
        else:
            print(f"[ARQUIVO CRIADO] {rel_path}")
            self.routes._check_and_upload(event.src_path, rel_path)

    def on_modified(self, event):
        if not event.is_directory:
            rel_path = self._relative_path(event.src_path)
            print(f"[ARQUIVO MODIFICADO] {rel_path}")
            self.routes._check_and_upload(event.src_path, rel_path)

    def on_deleted(self, event):
        rel_path = self._relative_path(event.src_path)
        print(f"[REMOVIDO] {rel_path}")
        self.routes._deleteFile(rel_path)
        print(f"[REMOVIDO DO SERVIDOR] {rel_path}")

    def on_moved(self, event):
        old_rel = self._relative_path(event.src_path)
        new_rel = self._relative_path(event.dest_path)
        print(f"[ARQUIVO MOVIDO] De: {old_rel} Para: {new_rel}")
        self.on_deleted(event)
        if not event.is_directory:
            self.routes._check_and_upload(event.dest_path, new_rel)
        
class ObserverDirectory:
    def __init__(self, directory_to_watch):
        self.directory_to_watch = os.path.abspath(directory_to_watch)
        self.ActionDirectory = ActionsDirectory(self.directory_to_watch)
        self.observer = Observer()

    def run(self):
        self.observer.schedule(self.ActionDirectory, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

   

   
            