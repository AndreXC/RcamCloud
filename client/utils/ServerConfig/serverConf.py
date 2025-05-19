
from dotenv import load_dotenv
import os

load_dotenv()
class serverConf:
    def __init__(self):
        self.server_url = os.getenv("SERVER_URL")
        self.folder = "folder"
        os.makedirs(self.folder, exist_ok=True)         
            


