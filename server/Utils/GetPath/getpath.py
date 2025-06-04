from pathlib import Path
import os


class DirectoryPathServer:
    def __init__(self):
        if os.path.exists("C:\\Users"):
            usuario = os.getlogin()
            self.client_path = Path(os.path.join("C:\\Users", usuario, "StorageServer"))
        else:
            self.client_path = Path("C:\\StorageServer")

    def get_path(self) -> Path:
        os.makedirs(self.client_path, exist_ok=True)
        return self.client_path
