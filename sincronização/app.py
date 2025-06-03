import os
import hashlib
from pathlib import Path
from typing import Dict, List

class FileHasher:
    """Responsável por gerar os hashes de arquivos"""
    @staticmethod
    def hash_file(path: str) -> str:
        sha256 = hashlib.sha256()
        try:
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except FileNotFoundError:
            return ''  # Arquivo inexistente

class DirectorySnapshot:
    """Responsável por mapear a estrutura de diretórios e seus hashes"""
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.snapshot = self._generate_snapshot()

    def _generate_snapshot(self) -> Dict[str, str]:
        snapshot = {}
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                full_path = Path(root) / file
                relative_path = str(full_path.relative_to(self.base_dir))
                file_hash = FileHasher.hash_file(full_path)
                snapshot[relative_path.replace("\\", "/")] = file_hash
        return snapshot

    def get_snapshot(self) -> Dict[str, str]:
        return self.snapshot
    
    
class DirectoryComparator:
    """Compara dois snapshots e detecta diferenças"""
    def __init__(self, local_snapshot: Dict[str, str], remote_snapshot: Dict[str, str]):
        self.local = local_snapshot
        self.remote = remote_snapshot

    def compare(self) -> Dict[str, List[str]]:
        missing_in_local = []
        hash_mismatch = []
        missing_in_server = []

        # Verifica o que está no servidor, mas não no cliente (ou está com hash diferente)
        for rel_path, remote_hash in self.remote.items():
            local_hash = self.local.get(rel_path)
            if local_hash is None:
                missing_in_local.append(rel_path)
            elif local_hash != remote_hash:
                hash_mismatch.append(rel_path)

        # Verifica o que está no cliente, mas não no servidor
        for rel_path in self.local:
            if rel_path not in self.remote:
                missing_in_server.append(rel_path)

        return {
            "missing_in_local": missing_in_local,     # deve ser baixado
            "hash_mismatch": hash_mismatch,           # deve ser baixado
            "missing_in_server": missing_in_server    # deve ser enviado
        }
