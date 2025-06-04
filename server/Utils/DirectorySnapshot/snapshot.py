import os
from pathlib import Path
from typing import Dict, List
from ..CalcHash.calcHash import FileHasher
from  ..GetPath.getpath import DirectoryPathServer
# from log.log  import LogRequest

class DirectorySnapshot:
    """Responsável por mapear a estrutura de diretórios e seus hashes"""
    def __init__(self):
        self.base_dir = DirectoryPathServer().get_path()

    def _generate_snapshot(self) -> Dict[str, str]:
        try:
            if not self.base_dir:
                return {[]}
            
            snapshot = {}
            for root, _, files in os.walk(self.base_dir):
                for file in files:
                    full_path = Path(root) / file
                    relative_path = str(full_path.relative_to(self.base_dir))
                    file_hash = FileHasher.hash_file(full_path)
                    snapshot[relative_path.replace("\\", "/")] = file_hash
            return snapshot
        except Exception as e:
            # LogRequest(f"Erro ao gerar snapshot do diretório: {str(e)}", 'servidor').request_log()
            return {[]}    
        
class DirectoryComparator:
    """Compara dois snapshots e detecta diferenças"""
    def __init__(self, local_snapshot: Dict[str, str], remote_snapshot: Dict[str, str]):
        self.local = local_snapshot
        self.remote = remote_snapshot

    def compare(self) -> Dict[str, List[str]]:
        try:
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
                "ausente_no_cliente": missing_in_local,   # deve ser baixado
                "Hashs_nao_equivalentes": hash_mismatch,  # deve ser baixado
                "ausente_no_server": missing_in_server    # deve ser enviado
            }
        except Exception as e:
            # LogRequest(f"Erro ao comparar snapshots: {str(e)}", 'servidor').request_log()
            return {}