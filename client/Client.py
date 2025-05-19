import os
import time
import hashlib
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SERVER_URL = "https://heavily-discrete-haddock.ngrok-free.app"
FOLDER = "./folder"
os.makedirs(FOLDER, exist_ok=True)

def calculate_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

class Watcher:
    def __init__(self, directory_to_watch):
        self.directory_to_watch = os.path.abspath(directory_to_watch)
        self.event_handler = Handler(self.directory_to_watch)
        self.observer = Observer()

    def run(self):
        self.observer.schedule(self.event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, base_path):
        self.base_path = base_path

    def _relative_path(self, full_path):
        return os.path.relpath(full_path, self.base_path).replace("\\", "/")  # cross-platform

    def on_created(self, event):
        rel_path = self._relative_path(event.src_path)
        if event.is_directory:
            print(f"[DIRETÓRIO CRIADO] {rel_path}")
            self._create_directory_on_server(rel_path)
        else:
            print(f"[ARQUIVO CRIADO] {rel_path}")
            self._check_and_upload(event.src_path, rel_path)

    def on_modified(self, event):
        if not event.is_directory:
            rel_path = self._relative_path(event.src_path)
            print(f"[ARQUIVO MODIFICADO] {rel_path}")
            self._check_and_upload(event.src_path, rel_path)

    def on_deleted(self, event):
        rel_path = self._relative_path(event.src_path)
        print(f"[REMOVIDO] {rel_path}")
        try:
            res = requests.delete(f"{SERVER_URL}/delete/{rel_path}")
            res.raise_for_status()
            print(f"[REMOVIDO DO SERVIDOR] {rel_path}")
        except requests.exceptions.RequestException as e:
            print(f"[ERRO AO DELETAR] {e}")

    def on_moved(self, event):
        old_rel = self._relative_path(event.src_path)
        new_rel = self._relative_path(event.dest_path)
        print(f"[ARQUIVO MOVIDO] De: {old_rel} Para: {new_rel}")
        self.on_deleted(event)
        if not event.is_directory:
            self._check_and_upload(event.dest_path, new_rel)

    def _create_directory_on_server(self, rel_path):
        try:
            res = requests.post(f"{SERVER_URL}/mkdir", json={"path": rel_path})
            res.raise_for_status()
            print(f"[DIRETÓRIO CRIADO NO SERVIDOR] {rel_path}")
        except requests.exceptions.RequestException as e:
            print(f"[ERRO AO CRIAR DIRETÓRIO] {e}")

    def _check_and_upload(self, filepath, rel_path):
        try:
            file_hash = calculate_file_hash(filepath)
        except Exception as e:
            print(f"[ERRO] Não foi possível calcular o hash: {e}")
            return

        try:
            res = requests.post(f"{SERVER_URL}/check_hash", json={
                "filename": rel_path,
                "sha256": file_hash
            })
            res.raise_for_status()
            match = res.json().get("match", False)

            if not match:
                with open(filepath, "rb") as f:
                    print(f"[UPLOAD] {rel_path}")
                    upload_res = requests.post(
                        f"{SERVER_URL}/upload",
                        files={"file": (rel_path, f)}
                    )
                    print(f"[RESULTADO] {upload_res.json()}")
            else:
                print(f"[SINCRONIZADO] {rel_path}")
        except requests.exceptions.RequestException as e:
            print(f"[ERRO DE REDE] {e}")

if __name__ == "__main__":
    watcher = Watcher(FOLDER)
    watcher.run()

print('teste')
