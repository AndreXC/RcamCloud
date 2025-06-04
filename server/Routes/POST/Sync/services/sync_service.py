from schemas.sync_shcemas import SnapshotModel
from Utils.DirectorySnapshot.snapshot import DirectorySnapshot, DirectoryComparator
from fastapi.responses import JSONResponse
from fastapi import status 
class SyncService:
    def CheckSync(self, data: SnapshotModel):
        try:
            client_snapshot = data.snapshot
            server_snapshot = DirectorySnapshot()._generate_snapshot()
            if not server_snapshot:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={'status': False, 
                             'message': 'Nenhum arquivo encontrado no servidor.',
                             'error': '', 
                             'data': {}
                            }
                )
            comparator = DirectoryComparator(server_snapshot, client_snapshot)
            result = comparator.compare()
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'status': True,
                    'message': 'Sincronização realizada com sucesso.',
                    'error': '',
                    'data': result
                }
            )
                    
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    'status': False,
                    'message': f'Erro ao realizar a sincronização',
                    'error': str(e),
                    'data': {}
                }
            )