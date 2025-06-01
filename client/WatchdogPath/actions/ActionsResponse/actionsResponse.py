from ...fila_arquivos.filaArquivos import FilaArquivosClient

class TratadorResposta:
    def __init__(self):
        self.fila = FilaArquivosClient()

    def tratar(self, resposta: dict, acao: str, dados: dict):
        if not resposta.get('status'):
            self.fila.add(acao, dados)
