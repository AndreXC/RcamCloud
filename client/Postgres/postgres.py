import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError
from log.log import LogRequest

class PostgresConnectionEnv:
    def __init__(self):
        # Carrega as variáveis de ambiente do arquivo .env
        load_dotenv()
        self.user = os.getenv('POSTGRES_USER')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.host = os.getenv('POSTGRES_HOST')
        self.port = int(os.getenv('POSTGRES_PORT', 5432))
        self.db_name = os.getenv('POSTGRES_DB_NAME')

class PostgresDB:
    def __init__(self):
        connection = PostgresConnectionEnv()
        self.user = connection.user
        self.password = connection.password
        self.host = connection.host
        self.port = connection.port
        self.db_name = connection.db_name
        
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
            LogRequest(f'Erro ao conectar ao banco de dados: {str(e)}', 'cliente').request_log()
            return {'status_conection': False, 'error': str(e), 'message': 'Erro ao conectar ao banco de dados.'}
        
    def execute(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            LogRequest(f'Erro ao executar a consulta: {str(e)}', 'cliente').request_log()
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



#Exemplo de uso:
    #conexão
        # db = PostgresDB()
        # db.connect()
    #execute uma consulta
        # db.execute("SELECT * FROM file_hashes;")    
    #recupere todos os resultados
       #result = db.fetchone()
    #fechar conexão
        # db.close()

