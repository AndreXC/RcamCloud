from datetime import datetime
from  Postgres.postgres import PostgresDB
from psycopg2.extras import Json

class FilaArquivosClient:
    def __init__(self):
        self.conn = PostgresDB()

    def add(self, action, args):
        try:
            """Adiciona uma ação à fila de retry."""
            now =  datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.conn.connect()
            self.conn.execute("""
                INSERT INTO retry_actions (action, args, timestamp, executado)
                VALUES (%s, %s, %s, FALSE)
            """, (action, Json(args), now))
            return {'status': True, 'message': 'Ação adicionada à fila com sucesso.'}
        except Exception as e:
            return {'status': False, 'error': str(e), 'message': 'Erro ao adicionar ação à fila.'}
        finally:
            self.conn.close()

    def get_pending(self):
        """Retorna todas as ações pendentes na fila."""
        try:
            self.conn.connect()
            self.conn.execute("""
                SELECT id, action, args FROM retry_actions
                WHERE executado = FALSE
                ORDER BY timestamp ASC
            """)
            return {'status': True, 'erro': '', 'data': self.conn.fetchall()}
        except Exception as e:
            return {'status': False, 'error': str(e), 'message': 'Erro ao buscar ações pendentes.'} 
        finally:
            self.conn.close()

        
    def mark_as_executed(self, action_id):
        """Marca uma ação como executada na fila."""
        try:
            self.conn.connect()
            self.conn.execute("""
                UPDATE retry_actions SET executado = TRUE WHERE id = %s
            """, (action_id,))
            return {'status': True, 'message': 'Ação realizada com Sucesso!'}
        except Exception as e:
            return {'status': False, 'error': str(e), 'message': 'Erro ao marcar ação como executada.'}
        finally:
            self.conn.close()            
        