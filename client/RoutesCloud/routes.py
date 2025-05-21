from utils.CalcHash.calcHash import calculate_file_hash
import requests
from utils.ServerConfig.serverConf import serverConf
from log.log import LogRequest
import traceback

class routesLink:
    def __init__(self):
        self.server_conf = serverConf()
        self.local_folder = self.server_conf.folder
        self.server_url = self.server_conf.server_url
        
        self.routeCreatedirectory = f"{self.server_url}/mkdir"
        self.routeCheckHash = f"{self.server_url}/check_hash"
        self.routeUpload = f"{self.server_url}/upload"
        self.routeDownload = f"{self.server_url}/download"
        self.routeDelete = f"{self.server_url}/delete"
        self.routeList = f"{self.server_url}/list" 

class routes:
    def __init__(self):
        self.routesLink = routesLink()
    
    def SendRequest(self, route, method, data=None):
        try:
            if method == "GET":
                response = requests.get(route)
            elif method == "POST":
                response = requests.post(route, json=data)
            elif method == "DELETE":
                response = requests.delete(route)
            else:
                raise ValueError("Método HTTP inválido.")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"{str(e)}\n{traceback.format_exc()}"
            LogRequest(error_message, 'cliente').request_log()
            return None

    def _create_directory_on_server(self, rel_path):
        try:
            response = self.SendRequest(self.routesLink.routeCreatedirectory, "POST", {"path": rel_path})            
            print(f"[DIRETÓRIO CRIADO NO SERVIDOR] {rel_path}")
        except Exception as e:
            error_message = f"{str(e)}\n{traceback.format_exc()}"
            LogRequest(error_message, 'cliente').request_log()
            print(f"[ERRO AO CRIAR DIRETÓRIO] {e}")
            
    def __checkHashRoute__(self, filepath, rel_path):
        try:
            file_hash = calculate_file_hash(filepath)
       
            response = self.SendRequest(self.routesLink.routeCheckHash, "POST", {
                "filename": rel_path,
                "sha256": file_hash
            })
            return response.get("match", False)
        except Exception as e:
            error_message = f"{str(e)}\n{traceback.format_exc()}"
            LogRequest(error_message, 'cliente').request_log()
            return False
    
    def _check_and_upload(self, filepath, rel_path):
        try:    
            match = self.__checkHashRoute__(filepath, rel_path)
            if not match:
                with open(filepath, "rb") as f:
                    print(f"[UPLOAD] {rel_path}")
                    response = self.SendRequest(self.routesLink.routeUpload, "POST", {
                        "file": (rel_path, f)
                    })
                    print(f"[RESULTADO] {response}")
            else:
                print(f"[SINCRONIZADO] {rel_path}")
        except Exception as e:
            error_message = f"{str(e)}\n{traceback.format_exc()}"
            LogRequest(error_message, 'cliente').request_log()
            print(f"[ERRO DE REDE] {e}")
            
    def _deleteFile(self, rel_path):
        try:
            response = self.SendRequest(self.routesLink.routeDelete, "DELETE", {"path": rel_path})
            print(f"[REMOVIDO DO SERVIDOR] {rel_path}")
        except Exception as e:
            error_message = f"{str(e)}\n{traceback.format_exc()}"
            LogRequest(error_message, 'cliente').request_log()
            print(f"[ERRO AO DELETAR] {e}")
    
        

