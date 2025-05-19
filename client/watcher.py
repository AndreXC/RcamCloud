# client/watcher.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import requests
import os

SERVER_URL = "http://localhost:8000"

class SyncHandler(FileSystemEventHandler):
    def __init__(self, folder):
        self.folder = folder

    def on_modified(self, event):
        if not event.is_directory:
            self.sync_file(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.sync_file(event.src_path)

    def sync_file(self, file_path):
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            print(f"Enviando {filename} para o servidor...")
            r = requests.post(f"{SERVER_URL}/upload", files={"file": (filename, f)})
            print(r.json())

def start_watching(folder):
    event_handler = SyncHandler(folder)
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=False)
    observer.start()
    print(f"Observando alterações em: {folder}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
