# import os
# import hashlib
# from fastapi import UploadFile, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select, insert, update
# from Model.HashModel.Hashmodel import FileHash

# UPLOAD_DIR = "storage"

# class FileProcessor:
#     def __init__(self, db: AsyncSession):
#         self.db = db

#     async def handle_file(self, file: UploadFile, input_hash: str) -> dict:
#         rel_path = file.filename.replace("\\", "/").lstrip("/")
#         file_path = os.path.join(UPLOAD_DIR, rel_path)

#         validation = self._validate_input(rel_path, input_hash)
#         if validation:
#             return validation

#         content = await file.read()
#         if not content:
#             return self._response(status.HTTP_400_BAD_REQUEST, False, "Arquivo vazio.", "Conteúdo não lido.")

#         calculated_hash = hashlib.sha256(content).hexdigest()

#         os.makedirs(os.path.dirname(file_path), exist_ok=True)

#         existing = await self._get_existing_file(rel_path)

#         if existing:
#             if existing.hash == calculated_hash:
#                 return self._response(status.HTTP_200_OK, True, None, "O arquivo já existe e é idêntico.")
#             await self._replace_file(file_path, content)
#             await self._update_hash(rel_path, calculated_hash)
#             return self._response(status.HTTP_200_OK, True, None, "Arquivo substituído. Hash atualizado.")
#         else:
#             await self._save_new_file(file_path, content)
#             await self._insert_file_hash(rel_path, calculated_hash)
#             return self._response(status.HTTP_201_CREATED, True, calculated_hash, "Novo arquivo salvo.")

#     def _validate_input(self, filename: str, sha256: str):
#         if not filename or not isinstance(filename, str):
#             return self._response(status.HTTP_400_BAD_REQUEST, False, None, "Nome do arquivo inválido.")
#         if not sha256 or not isinstance(sha256, str) or len(sha256) != 64:
#             return self._response(status.HTTP_400_BAD_REQUEST, False, None, "Hash SHA256 inválido.")
#         return None

#     async def _get_existing_file(self, filename: str):
#         stmt = select(FileHash).where(FileHash.filename == filename)
#         result = await self.db.execute(stmt)
#         return result.scalar_one_or_none()

#     async def _update_hash(self, filename: str, sha256: str):
#         stmt = update(FileHash).where(FileHash.filename == filename).values(hash=sha256)
#         await self.db.execute(stmt)
#         await self.db.commit()

#     async def _insert_file_hash(self, filename: str, sha256: str):
#         stmt = insert(FileHash).values(filename=filename, hash=sha256)
#         await self.db.execute(stmt)
#         await self.db.commit()

#     async def _replace_file(self, path: str, content: bytes):
#         with open(path, "wb") as f:
#             f.write(content)

#     async def _save_new_file(self, path: str, content: bytes):
#         with open(path, "wb") as f:
#             f.write(content)

#     def _response(self, status_code: int, status_val: bool, hash_val: str, message: str):
#         return {
#             "status_code": status_code,
#             "content": {
#                 "status": status_val,
#                 "hash": hash_val,
#                 "message": message
#             }
#         }


import os
import hashlib
from fastapi import UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from Model.HashModel.Hashmodel import FileHash

UPLOAD_DIR = "storage"

class FileProcessor:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def handle_file(self, file: UploadFile, File_hash: str) -> dict:
        try:
            rel_path = file.filename.replace("\\", "/").lstrip("/")
            file_path = os.path.join(UPLOAD_DIR, rel_path)

            error = self._validate_input(rel_path, File_hash)
            if error:
                return error

            content = await file.read()
            if not content:
                return self.__response__(status.HTTP_400_BAD_REQUEST, False, "Arquivo vazio.", "Conteúdo não lido.")

            calculated_hash = hashlib.sha256(content).hexdigest()
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            existing = await self._get_existing_file(rel_path)

            if existing:
                if existing.hash == calculated_hash:
                    return self.__response__(status.HTTP_200_OK, True, "", "O arquivo já existe e é idêntico.")
                await self._write_file(file_path, content)
                await self._update_hash(rel_path, calculated_hash)
                return self.__response__(status.HTTP_200_OK, True, "", "Arquivo substituído. Hash atualizado.")
            else:
                await self._write_file(file_path, content)
                await self._insert_file_hash(rel_path, calculated_hash)
                return self.__response__(status.HTTP_201_CREATED, True, "", "Novo arquivo salvo.")
        
        except Exception as e:
            await self.db.rollback()
            return self.__response__(status.HTTP_500_INTERNAL_SERVER_ERROR, False, , "Erro inesperado no processamento do arquivo.")

    def _validate_input(self, filename: str, File_hash: str):
        if not File_hash:
            return self.__response__(status.HTTP_400_BAD_REQUEST, False, "Hash SHA256 não fornecido.")
        if not filename or not isinstance(filename, str):
            return self.__response__(status.HTTP_400_BAD_REQUEST, False, "Nome do arquivo inválido.")
        if not File_hash or not isinstance(File_hash, str) or len(File_hash) != 64:
            return self.__response__(status.HTTP_400_BAD_REQUEST, False, "Hash SHA256 inválido.")
        return None

    async def _get_existing_file(self, filename: str):
        stmt = select(FileHash).where(FileHash.filename == filename)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def _update_hash(self, filename: str, sha256: str):
        stmt = update(FileHash).where(FileHash.filename == filename).values(hash=sha256)
        await self.db.execute(stmt)
        await self.db.commit()

    async def _insert_file_hash(self, filename: str, sha256: str):
        stmt = insert(FileHash).values(filename=filename, hash=sha256)
        await self.db.execute(stmt)
        await self.db.commit()

    async def _write_file(self, path: str, content: bytes):
        with open(path, "wb") as f:
            f.write(content)

    def __response__(self, status_code: int, status_val: bool, error_msg: str, message: str = ""):
        return {
            "status_code": status_code,
            "status": status_val,
            "error": error_msg,
            "message": message or "Erro inesperado no processamento do arquivo."
        }
