import hashlib
import os
import traceback
from log.log import LogRequest

class FileHasher:
    """Responsável por gerar os hashes de arquivos"""

    @staticmethod
    def _get_block_size(file_size: int) -> int:
        """
        Define o tamanho ideal do bloco de leitura com base no tamanho do arquivo.
        """
        match file_size:
            case size if size <= 1 * 1024 * 1024:             # ≤ 1 MB
                return 4096                                   # 4 KB
            case size if size <= 100 * 1024 * 1024:           # ≤ 100 MB
                return 8192                                   # 8 KB
            case size if size <= 1 * 1024 * 1024 * 1024:      # ≤ 1 GB
                return 32768                                  # 32 KB
            case _:
                return 65536                                  # > 1 GB → 64 KB

    @staticmethod
    def hash_file(Filepath: str) -> str:
        sha256 = hashlib.sha256()
        try:
            file_size = os.path.getsize(Filepath)
            block_size = FileHasher._get_block_size(file_size)

            with open(Filepath, 'rb') as f:
                for byte_block in iter(lambda: f.read(block_size), b''):
                    sha256.update(byte_block)

            return sha256.hexdigest()
        except Exception as e:
            LogRequest(
                f"Erro ao calcular hash do arquivo {Filepath}: {str(e)}\n{traceback.format_exc()}",
                'cliente'
            ).request_log()
            return ''



# def calculate_file_hash(filepath):
#     try:
#         sha256_hash = hashlib.sha256()
#         with open(filepath, "rb") as f:
#             for byte_block in iter(lambda: f.read(4096), b""):
#                 sha256_hash.update(byte_block)
#         return sha256_hash.hexdigest() 
#     except Exception as e:
#         LogRequest(f"Erro ao calcular hash do arquivo {filepath}: {str(e)}\n{traceback.format_exc()}", 'cliente').request_log()
#         return None

