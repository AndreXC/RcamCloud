# import os
# import requests
# from pathlib import Path
# from .app import DirectorySnapshot
# import mimetypes

# SERVER_URL = "http://localhost:8000"
# CLIENT_BASE = Path("meu_dir")


# def baixar_arquivo_estruturado(rel_path: str):
#     url = f"{SERVER_URL}/download?file={rel_path}"
#     response = requests.get(url)

#     if response.status_code == 200:
#         destino = CLIENT_BASE / rel_path
#         destino.parent.mkdir(parents=True, exist_ok=True)
#         with open(destino, 'wb') as f:
#             f.write(response.content)
#         print(f"[OK] Baixado: {rel_path}")
#     else:
#         print(f"[ERRO] Falha ao baixar: {rel_path}")


# def enviar_arquivo_para_servidor(rel_path: str):
#     caminho_local = CLIENT_BASE / rel_path
#     url = f"{SERVER_URL}/upload"
#     if not caminho_local.exists():
#         print(f"[IGNORADO] Arquivo inexistente localmente: {rel_path}")
#         return

#     with open(caminho_local, "rb") as f:
#         mime_type, _ = mimetypes.guess_type(str(caminho_local))
#         files = {"file": (rel_path, f, mime_type or "application/octet-stream")}
#         data = {"rel_path": rel_path}
#         response = requests.post(url, files=files, data=data)

#     if response.status_code == 200:
#         print(f"[OK] Enviado: {rel_path}")
#     else:
#         print(f"[ERRO] Falha ao enviar: {rel_path}")


# def sincronizar():
#     local_snapshot = DirectorySnapshot(CLIENT_BASE).get_snapshot()
#     response = requests.post(f"{SERVER_URL}/sync", json={"snapshot": local_snapshot})

#     if response.status_code != 200:
#         print("Erro ao sincronizar com o servidor.")
#         return

#     diffs = response.json()

#     arquivos_para_baixar = diffs.get("missing_in_local", []) + diffs.get("hash_mismatch", [])
#     arquivos_para_enviar = diffs.get("missing_in_server", [])

#     for arquivo in arquivos_para_baixar:
#         baixar_arquivo_estruturado(arquivo)

#     for arquivo in arquivos_para_enviar:
#         enviar_arquivo_para_servidor(arquivo)


# if __name__ == "__main__":
#     sincronizar()


import os
import requests
import mimetypes
from pathlib import Path
from .app import DirectorySnapshot


class FileSyncClient:
    def __init__(self, server_url: str, client_base: Path):
        self.server_url = server_url.rstrip("/")
        self.client_base = client_base

    def _log(self, msg: str, status: str = "INFO"):
        print(f"[{status}] {msg}")

    def baixar_arquivo(self, rel_path: str):
        url = f"{self.server_url}/download?file={rel_path}"
        response = requests.get(url)

        if response.ok:
            destino = self.client_base / rel_path
            destino.parent.mkdir(parents=True, exist_ok=True)
            with open(destino, 'wb') as f:
                f.write(response.content)
            self._log(f"Baixado: {rel_path}", "OK")
        else:
            self._log(f"Falha ao baixar: {rel_path}", "ERRO")

    def enviar_arquivo(self, rel_path: str):
        caminho_local = self.client_base / rel_path

        if not caminho_local.exists():
            self._log(f"Arquivo inexistente localmente: {rel_path}", "IGNORADO")
            return

        url = f"{self.server_url}/upload"
        mime_type, _ = mimetypes.guess_type(str(caminho_local))

        with open(caminho_local, "rb") as f:
            files = {"file": (rel_path, f, mime_type or "application/octet-stream")}
            data = {"rel_path": rel_path}
            response = requests.post(url, files=files, data=data)

        if response.ok:
            self._log(f"Enviado: {rel_path}", "OK")
        else:
            self._log(f"Falha ao enviar: {rel_path}", "ERRO")

    def sincronizar(self):
        snapshot = DirectorySnapshot(self.client_base).get_snapshot()
        response = requests.post(f"{self.server_url}/sync", json={"snapshot": snapshot})

        if not response.ok:
            self._log("Erro ao sincronizar com o servidor.", "ERRO")
            return

        diffs = response.json()
        arquivos_para_baixar = diffs.get("missing_in_local", []) + diffs.get("hash_mismatch", [])
        arquivos_para_enviar = diffs.get("missing_in_server", [])

        for arquivo in arquivos_para_baixar:
            self.baixar_arquivo(arquivo)

        for arquivo in arquivos_para_enviar:
            self.enviar_arquivo(arquivo)


if __name__ == "__main__":
    # Configuração padrão
    sync_client = FileSyncClient(server_url="http://localhost:8000", client_base=Path("meu_dir"))
    sync_client.sincronizar()
