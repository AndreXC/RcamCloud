import os
import json

class TokenManager:
    def __init__(self):
        self.folderName = 'TokenRcamCloud'
        self.file_name= 'tokenApi.json'
        self.appdata_dir = os.getenv('APPDATA') or os.path.expanduser("~/.config")
        self.token_dir = os.path.join(self.appdata_dir, self.folderName)
        self.token_file = os.path.join(self.token_dir, self.file_name)
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs(self.token_dir, exist_ok=True)
        if not os.path.isfile(self.token_file):
            with open(self.token_file, 'w', encoding='utf-8') as f:
                json.dump({"token": ""}, f, indent=4)

    def get_token(self):
        with open(self.token_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("token", "")

    def set_token(self, novo_token):
        with open(self.token_file, 'w', encoding='utf-8') as f:
            json.dump({"token": novo_token}, f, indent=4)

    def get_token_path(self):
        return self.token_file
    