import hashlib
import traceback
from log.log import LogRequest
def calculate_file_hash(filepath):
    try:
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest() 
    except Exception as e:
        LogRequest(f"Erro ao calcular hash do arquivo {filepath}: {str(e)}\n{traceback.format_exc()}", 'cliente').request_log()
        return None

