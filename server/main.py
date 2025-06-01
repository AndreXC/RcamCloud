# # server/main.py
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.responses import FileResponse
# import os
# from pydantic import BaseModel
# import hashlib

# app = FastAPI()
# UPLOAD_DIR = "server/storage"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# hash_registry = {}


# class FileHashRequest(BaseModel):
#     filename: str
#     sha256: str


# @app.post("/check_hash")
# def check_hash(info: FileHashRequest):
#     stored_hash = hash_registry.get(info.filename)
#     return {"match": stored_hash == info.sha256}

# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     contents = await file.read()
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
    
#     sha256 = hashlib.sha256(contents).hexdigest()
    
#     # salvar arquivo
#     with open(file_path, "wb") as f:
#         f.write(contents)
    
#     hash_registry[file.filename] = sha256
#     return {"status": "uploaded", "hash": sha256}


# @app.get("/download/{filename}")
# def download_file(filename: str):
#     file_path = os.path.join(UPLOAD_DIR, filename)
#     return FileResponse(file_path)

# @app.get("/list")
# def list_files():
#     return {"files": os.listdir(UPLOAD_DIR)}



# @app.delete("/delete/{filename}")
# def delete_file(filename: str):
#     file_path = os.path.join(UPLOAD_DIR, filename)

#     if not os.path.isfile(file_path):
#         raise HTTPException(status_code=404, detail="Arquivo não encontrado")

#     try:
#         os.remove(file_path)
#         hash_registry.pop(filename, None)
#         return {"status": "deleted", "filename": filename}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Erro ao deletar arquivo: {str(e)}") 


# from fastapi import FastAPI, UploadFile, File, HTTPException, status
# from fastapi.responses import FileResponse, JSONResponse
# from pydantic import BaseModel
# import os
# import hashlib
# import shutil

# app = FastAPI()

# UPLOAD_DIR = "server/storage"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# hash_registry = {}

# # class FileHashRequest(BaseModel):
# #     filename: str  # agora é caminho relativo (ex: subpasta/arquivo.txt)
# #     sha256: str


# class DirectoryRequest(BaseModel):
#     path: str  # caminho relativo do diretório


# @app.post("/check_hash")
# def check_hash(info: FileHashRequest):
#     try:
#         if not info.filename or not isinstance(info.filename, str):
#             return JSONResponse(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 content={
#                     "status": False,
#                     "match": None,
#                     "error": "Nome do arquivo inválido.",
#                     "message": "O campo 'filename' deve ser uma string não vazia."
#                 }
#             )
#         if not info.sha256 or not isinstance(info.sha256, str) or len(info.sha256) != 64:
#             return JSONResponse(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 content={
#                     "status": False,
#                     "match": None,
#                     "error": "Hash SHA256 inválido.",
#                     "message": "O campo 'sha256' deve ser uma string hexadecimal de 64 caracteres."
#                 }
#             )

#         stored_hash = hash_registry.get(info.filename)
#         if stored_hash is None:
#             return JSONResponse(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 content={
#                     "status": False,
#                     "match": None,
#                     "error": "Arquivo não encontrado.",
#                     "message": f"O arquivo '{info.filename}' não está registrado no servidor."
#                 }
#             )

#         match = stored_hash == info.sha256
#         return JSONResponse(
#             status_code=status.HTTP_200_OK,
#             content={
#                 "status": True,
#                 "match": match,
#                 "filename": info.filename,
#                 "message": "Hash confere." if match else "Hash não confere."
#             }
#         )
#     except Exception as e:
#         return JSONResponse(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content={
#                 "status": False,
#                 "match": None,
#                 "error": str(e),
#                 "message": "Erro ao verificar hash."
#             }
#         )


# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     try:
#         rel_path = file.filename.replace("\\", "/").lstrip("/")
#         file_path = os.path.join(UPLOAD_DIR, rel_path)
#         os.makedirs(os.path.dirname(file_path), exist_ok=True)
#         contents = await file.read()
        
#         if not contents:
#             return JSONResponse(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 content={
#                     "status": False,
#                     "error": "Arquivo vazio.",
#                     "message": "não foi possivel ler o arquivo enviado."
#                 }
#             )

#         sha256 = hashlib.sha256(contents).hexdigest()

#         with open(file_path, "wb") as f:
#             f.write(contents)

#         hash_registry[rel_path] = sha256

#         return JSONResponse(
#             status_code=status.HTTP_200_OK,
#             content={
#                 "status": True,
#                 "hash": sha256,
#                 "path": rel_path,
#                 "message": "Arquivo enviado com sucesso."
#             }
#         )
#     except Exception as e:
#         return JSONResponse(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content={
#                 "status": False,
#                 "error": str(e),
#                 "message": "Erro ao fazer upload do arquivo."
#             }
#         )



# @app.post("/mkdir")
# def create_directory(data: DirectoryRequest):
#     dir_path = os.path.join(UPLOAD_DIR, data.path)
#     try:
#         if os.path.exists(dir_path):
#             return JSONResponse(
#                 status_code=status.HTTP_201_CREATED,
#                 content={
#                     "status": True,
#                     "error": "",
#                     "directory": data.path,
#                     "message": f"Diretório já existe: {data.path}"
#                 }
#             )
#         os.makedirs(dir_path)
#         return JSONResponse(
#             status_code=status.HTTP_200_OK,
#             content={
#                 "status": True,
#                 "error": "",
#                 "directory": data.path,
#                 "message": f"Diretório criado com sucesso: {data.path}"
#             }
#             )
#     except Exception as e:
#         return JSONResponse(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content={
#                 "status": False,
#                 "error": str(e),
#                 "directory": data.path,
#                 "message": f"Erro ao criar diretório: {str(e)}"
#             }
#         )
    

# @app.delete("/delete/{filepath:path}")
# def delete_file(filepath: str):
#     target_path = os.path.join(UPLOAD_DIR, filepath)

#     if os.path.isdir(target_path):
#         try:
#             shutil.rmtree(target_path)
#             return {"status": "deleted", "directory": filepath}
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Erro ao deletar diretório: {str(e)}")

#     elif os.path.isfile(target_path):
#         try:
#             os.remove(target_path)
#             hash_registry.pop(filepath, None)
#             return {"status": "deleted", "file": filepath}
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Erro ao deletar arquivo: {str(e)}")
#     else:
#         raise HTTPException(status_code=404, detail="Arquivo ou diretório não encontrado")


# @app.get("/download/{filepath:path}")
# def download_file(filepath: str):
#     file_path = os.path.join(UPLOAD_DIR, filepath)

#     if not os.path.isfile(file_path):
#         raise HTTPException(status_code=404, detail="Arquivo não encontrado")

#     return FileResponse(file_path, filename=os.path.basename(file_path))


# @app.get("/DownloadAllArq")
# def list_files():
#     file_list = []
#     for root, _, files in os.walk(UPLOAD_DIR):
#         for file in files:
#             rel_dir = os.path.relpath(root, UPLOAD_DIR)
#             rel_file = os.path.normpath(os.path.join(rel_dir, file))
#             file_list.append(rel_file.replace("\\", "/"))
#     return {"files": file_list}
            
            


from fastapi import FastAPI
from Routes.DELETE.DeleteArq.ControllerDeleteArq import router as ControllerDeleteArq
from Routes.GET.DownloadFiles.ControllerDownloadFiles import router as ControllerDownloadFiles
from Routes.GET.DownloadAllFiles.ControllerDonwloadAllFiles import router as ControllerDonwloadAllFiles
from Routes.POST.CheckHash.ControllerHash import router as ControllerHash
from Routes.POST.CreateDir.ControllerCreateDir import router as ControllerCreateDir
from Routes.POST.UploadFile.ControllerUpload import router as ControllerUpload

app = FastAPI()

app.include_router(ControllerHash, prefix="/api", tags=["Hash"])
app.include_router(ControllerUpload, prefix="/api", tags=["Upload"])
app.include_router(ControllerCreateDir, prefix="/api", tags=["Diretório"])
app.include_router(ControllerDeleteArq, prefix="/api", tags=["Deleção"])
app.include_router(ControllerDownloadFiles, prefix="/api", tags=["Download"])
app.include_router(ControllerDonwloadAllFiles, prefix="/api", tags=["Listagem"])
