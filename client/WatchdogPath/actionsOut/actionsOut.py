from Postgres.postgres import PostgresDB

class AcoesRealizadas:
    def __init__(self):
        self.conn = PostgresDB()

    def list(self):
        """
        Retorna todas as ações registradas, ordenadas pela data.
        """
        try:
            self.conn.connect()
            self.conn.execute("""
                SELECT id, acao, data_acao
                FROM historico_acoes
                ORDER BY data_acao ASC
            """)
            return {
                'status': True,
                'erro': '',
                'dados': self.conn.fetchall()
            }
        except Exception as e:
            return {
                'status': False,
                'erro': str(e),
                'mensagem': 'Erro ao buscar ações realizadas.'
            }
        finally:
            self.conn.close()

    def add(self, acao: str):
        """
        Registra uma nova ação no histórico.
        """
        try:
            self.conn.connect()
            self.conn.execute("""
                INSERT INTO historico_acoes (acao)
                VALUES (%s)
            """, (acao,))
            return {
                'status': True,
                'mensagem': 'Ação registrada com sucesso.'
            }
        except Exception as e:
            return {
                'status': False,
                'erro': str(e),
                'mensagem': 'Erro ao registrar ação.'
            }
        finally:
            self.conn.close()
