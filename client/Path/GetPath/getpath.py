from pathlib import Path
import os
from models.usuario.session.User_session import UserObject

class DirectoryPathClient:
    def __init__(self):
        self.client_path = Path(f"C:/{UserObject.nome_diretorio}")  if UserObject else ''

    def get_path(self) -> Path:
        if self.client_path == '':
            return ''
        
        if not self.client_path.exists():
            os.makedirs(self.client_path)
        return self.client_path            
        
    