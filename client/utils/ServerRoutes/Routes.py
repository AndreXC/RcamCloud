
from dotenv import load_dotenv
import os

load_dotenv()
class RoutesServer:
    def __init__(self):
        self.server_url = os.getenv('SERVER_URL')
        self.routeList = f"{self.server_url}/list"
        self.routeDownload = f"{self.server_url}/download"
        self.routeUpload = f"{self.server_url}/upload"
        self.routeDelete = f"{self.server_url}/delete"
        self.routeCreateDirectory = f"{self.server_url}/mkdir"
        self.routeCheckHash = f"{self.server_url}/verificar-hash"
        self.DownloadAllArq  = f"{self.server_url}/DownloadAllArq"
        


            


