import os
import requests
from pathlib import Path
from .app import DirectorySnapshot
import mimetypes

SERVER_URL = "http://localhost:8000"
CLIENT_BASE = Path("meu_dir")


def baixar_arquivo_estruturado(rel_path: str):
    url = f"{SERVER_URL}/download?file={rel_path}"
    response = requests.get(url)

    if response.status_code == 200:
        destino = CLIENT_BASE / rel_path
        destino.parent.mkdir(parents=True, exist_ok=True)
        with open(destino, 'wb') as f:
            f.write(response.content)
        print(f"[OK] Baixado: {rel_path}")
    else:
        print(f"[ERRO] Falha ao baixar: {rel_path}")


def enviar_arquivo_para_servidor(rel_path: str):
    caminho_local = CLIENT_BASE / rel_path
    url = f"{SERVER_URL}/upload"
    if not caminho_local.exists():
        print(f"[IGNORADO] Arquivo inexistente localmente: {rel_path}")
        return

    with open(caminho_local, "rb") as f:
        mime_type, _ = mimetypes.guess_type(str(caminho_local))
        files = {"file": (rel_path, f, mime_type or "application/octet-stream")}
        data = {"rel_path": rel_path}
        response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        print(f"[OK] Enviado: {rel_path}")
    else:
        print(f"[ERRO] Falha ao enviar: {rel_path}")


def sincronizar():
    local_snapshot = DirectorySnapshot(CLIENT_BASE).get_snapshot()
    response = requests.post(f"{SERVER_URL}/sync", json={"snapshot": local_snapshot})

    if response.status_code != 200:
        print("Erro ao sincronizar com o servidor.")
        return

    diffs = response.json()

    arquivos_para_baixar = diffs.get("missing_in_local", []) + diffs.get("hash_mismatch", [])
    arquivos_para_enviar = diffs.get("missing_in_server", [])

    for arquivo in arquivos_para_baixar:
        baixar_arquivo_estruturado(arquivo)

    for arquivo in arquivos_para_enviar:
        enviar_arquivo_para_servidor(arquivo)


if __name__ == "__main__":
    sincronizar()
