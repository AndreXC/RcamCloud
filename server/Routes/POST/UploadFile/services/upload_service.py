# # import os
# # import hashlib
# # from fastapi import UploadFile, status
# # from fastapi.responses import JSONResponse
# # from sqlalchemy.ext.asyncio import AsyncSession
# # from Model.HashModel.Hashmodel import FileHash
# # from sqlalchemy import insert

# # UPLOAD_DIR = "storage"  # ajuste conforme necessário

# # class UploadService:
# #     def __init__(self, db: AsyncSession):
# #         self.db = db
        
# #     async def Valide_filename_Sha256(self, filename: str, sha256: str):
# #         if not filename or not isinstance(filename, str):
# #             return JSONResponse(
# #                 status_code=status.HTTP_400_BAD_REQUEST,
# #                 content={
# #                     "status": False,
# #                     "match": False,
# #                     "error": "Nome do arquivo inválido.",
# #                     "message": "O campo 'filename' deve ser uma string não vazia."
# #                 }
# #             )
# #         if not sha256 or not isinstance(sha256, str) or len(sha256) != 64:
# #             return JSONResponse(
# #                 status_code=status.HTTP_400_BAD_REQUEST,
# #                 content={
# #                     "status": False,
# #                     "match": False,
# #                     "error": "Hash SHA256 inválido.",
# #                     "message": "O campo 'sha256' deve ser uma string hexadecimal de 64 caracteres."
# #                 }
# #             )
# #         return None
    
# #      async def check(self, info: FileHashRequest) -> JSONResponse:
# #         try:
# #             error_response = await self.validate_input(info.filename, info.sha256)
# #             if error_response:
# #                 return error_response

# #             stmt = select(FileHash).where(FileHash.filename == info.filename)
# #             result = await self.db_session.execute(stmt)
# #             file_hash = result.scalar_one_or_none()

# #             if file_hash is None:
# #                 return JSONResponse(
# #                     status_code=status.HTTP_404_NOT_FOUND,
# #                     content={
# #                         "status": True,
# #                         "match": False,
# #                         "error": "Arquivo não encontrado.",
# #                         "message": f"O arquivo '{info.filename}' não está registrado no servidor."
# #                     }
# #                 )

# #             match = file_hash.hash == info.sha256
# #             return JSONResponse(
# #                 status_code=status.HTTP_200_OK,
# #                 content={
# #                     "status": True,
# #                     "match": match,
# #                     "filename": info.filename,
# #                     "message": "Hash confere." if match else "Hash não confere."
# #                 }
# #             )

# #         except Exception as e:
# #             return JSONResponse(
# #                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #                 content={
# #                     "status": False,
# #                     "match": False,
# #                     "error": str(e),
# #                     "message": "Erro ao verificar hash."
# #                 }
# #             )

# #     async def process_file(self, file: UploadFile, file_hash: str) -> JSONResponse:
# #         try:
# #             error_response = await self.validate_input(file.filename, file_hash)
# #             if error_response:
# #                 return error_response

# #             rel_path = file.filename.replace("\\", "/").lstrip("/")
# #             file_path = os.path.join(UPLOAD_DIR, rel_path)
# #             os.makedirs(os.path.dirname(file_path), exist_ok=True)

# #             contents = await file.read()
# #             if not contents:
# #                 return JSONResponse(
# #                     status_code=status.HTTP_400_BAD_REQUEST,
# #                     content={
# #                         "status": False,
# #                         "error": "Arquivo vazio.",
# #                         "message": "Não foi possível ler o arquivo enviado."
# #                     }
# #                 )

# #             sha256 = hashlib.sha256(contents).hexdigest()

# #             with open(file_path, "wb") as f:
# #                 f.write(contents)

# #             # Salvar no banco de dados
# #             stmt = insert(FileHash).values(filename=rel_path, hash=sha256)
# #             await self.db.execute(stmt)
# #             await self.db.commit()

# #             return JSONResponse(
# #                 status_code=status.HTTP_200_OK,
# #                 content={
# #                     "status": True,
# #                     "hash": sha256,
# #                     "path": rel_path,
# #                     "message": "Arquivo enviado com sucesso."
# #                 }
# #             )
# #         except Exception as e:
# #             await self.db.rollback()
# #             return JSONResponse(
# #                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #                 content={
# #                     "status": False,
# #                     "error": str(e),
# #                     "message": "Erro ao fazer upload do arquivo."
# #                 }
# #             )


# import os
# import hashlib
# from fastapi import UploadFile, status
# from fastapi.responses import JSONResponse
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import insert, update, select
# from Model.HashModel.Hashmodel import FileHash

# UPLOAD_DIR = "storage"

# class UploadService:
#     def __init__(self, db: AsyncSession):
#         self.db = db

#     async def validate_input(self, filename: str, sha256: str):
#         if not filename or not isinstance(filename, str):
#             return JSONResponse(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 content={
#                     "status": False,
#                     "match": False,
#                     "error": "Nome do arquivo inválido.",
#                     "message": "O campo 'filename' deve ser uma string não vazia."
#                 }
#             )
#         if not sha256 or not isinstance(sha256, str) or len(sha256) != 64:
#             return JSONResponse(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 content={
#                     "status": False,
#                     "match": False,
#                     "error": "Hash SHA256 inválido.",
#                     "message": "O campo 'sha256' deve ser uma string hexadecimal de 64 caracteres."
#                 }
#             )
#         return None

#     async def process_file(self, file: UploadFile, file_hash: str) -> JSONResponse:
#         try:
#             # Valida entrada
#             error_response = await self.validate_input(file.filename, file_hash)
#             if error_response:
#                 return error_response

#             rel_path = file.filename.replace("\\", "/").lstrip("/")
#             file_path = os.path.join(UPLOAD_DIR, rel_path)
#             os.makedirs(os.path.dirname(file_path), exist_ok=True)

#             contents = await file.read()
#             if not contents:
#                 return JSONResponse(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     content={
#                         "status": False,
#                         "error": "Arquivo vazio.",
#                         "message": "Não foi possível ler o arquivo enviado."
#                     }
#                 )

#             calculated_hash = hashlib.sha256(contents).hexdigest()

#             # Verifica se já existe no banco
#             stmt = select(FileHash).where(FileHash.filename == rel_path)
#             result = await self.db.execute(stmt)
#             existing_file = result.scalar_one_or_none()

#             if existing_file:
#                 if existing_file.hash == calculated_hash:
#                     return JSONResponse(
#                         status_code=status.HTTP_200_OK,
#                         content={
#                             "status": True,
#                             "match": True,
#                             "path": rel_path,
#                             "message": "O arquivo já existe e é idêntico ao enviado."
#                         }
#                     )
#                 else:
#                     # Substitui o arquivo e atualiza hash no banco
#                     with open(file_path, "wb") as f:
#                         f.write(contents)

#                     stmt_update = update(FileHash).where(FileHash.filename == rel_path).values(hash=calculated_hash)
#                     await self.db.execute(stmt_update)
#                     await self.db.commit()

#                     return JSONResponse(
#                         status_code=status.HTTP_200_OK,
#                         content={
#                             "status": True,
#                             "match": False,
#                             "path": rel_path,
#                             "message": "Arquivo substituído com novo conteúdo e hash atualizado."
#                         }
#                     )
#             else:
#                 # Novo arquivo
#                 with open(file_path, "wb") as f:
#                     f.write(contents)

#                 stmt_insert = insert(FileHash).values(filename=rel_path, hash=calculated_hash)
#                 await self.db.execute(stmt_insert)
#                 await self.db.commit()

#                 return JSONResponse(
#                     status_code=status.HTTP_201_CREATED,
#                     content={
#                         "status": True,
#                         "path": rel_path,
#                         "hash": calculated_hash,
#                         "message": "Novo arquivo salvo com sucesso."
#                     }
#                 )

#         except Exception as e:
#             await self.db.rollback()
#             return JSONResponse(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 content={
#                     "status": False,
#                     "error": str(e),
#                     "message": "Erro ao processar o upload do arquivo."
#                 }
#             )


from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from .processamento.file_processor import FileProcessor

class UploadService:
    def __init__(self, db: AsyncSession):
        self.processor = FileProcessor(db)

    async def process_file(self, File: UploadFile, File_Hash: str):
        try:
            result = await self.processor.handle_file(File, File_Hash)
            return JSONResponse(status_code=result["status_code"], content=result)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"status": False, "error": str(e), "message": "Erro inesperado no processamento do arquivo."}
            )
