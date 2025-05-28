import psycopg2
from psycopg2 import sql, OperationalError


class PostgresDB:
    def __init__(self, db_name:str, user:str, password:str, host:str, port:int):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor()
        except OperationalError as e:
            return {'status_conection': False, 'error': str(e), 'message': 'Erro ao conectar ao banco de dados.'}
        
    def execute(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            return {'status': False, 'error': str(e), 'message': 'Erro ao executar a consulta.'}
        
    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


# if __name__ == "__main__":
#     db = PostgresDB(
#         db_name="teste",
#         user="postgres",
#         password="postgres",
#         host="localhost",
#         port=5432
#     )

#     db.connect()
#     db.execute("SELECT * from file_hashes;")
#     result = db.fetchone()
#     print("Versão do PostgreSQL:", result)
#     db.close()
