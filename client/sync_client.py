# client/sync_client.py
import requests
import os

SERVER_URL = "http://localhost:8000"
LOCAL_FOLDER = "client/local_folder"

os.makedirs(LOCAL_FOLDER, exist_ok=True)

def sync_from_server():
    files = requests.get(f"{SERVER_URL}/list").json()["files"]
    for filename in files:
        local_path = os.path.join(LOCAL_FOLDER, filename)
        if not os.path.exists(local_path):
            print(f"Baixando {filename}...")
            r = requests.get(f"{SERVER_URL}/download/{filename}")
            with open(local_path, "wb") as f:
                f.write(r.content)

if __name__ == "__main__":
    sync_from_server()
