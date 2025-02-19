# db/postgre_conector.py
import os
from psycopg_pool import ConnectionPool
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

# Carrega as variáveis do .env
load_dotenv()


db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT")

class PostgreDatabaseManager:
    def __init__(self):
        # Apenas uma variável para o pool de conexões (inicialmente None)
        self.pool: ConnectionPool = None

    def start_pool(self):
        """
        Inicializa o pool de conexões usando as variáveis de ambiente.
        """
        conn_info = (
            f"dbname={db_name} "
            f"user={db_user} "
            f"password={db_pass} "
            f"host={db_host} "
            f"port={db_port}"
        )
        try:
            self.pool = ConnectionPool(
                conninfo=conn_info,
                min_size=int(1),
                max_size=int(10)
            )
        except Exception as e:
            raise

    def get_connection(self):
        """
        Obtém uma conexão do pool.
        """
        if self.pool is None:
            raise Exception("Pool não iniciado. Chame start_pool() primeiro.")
        try:
            conn = self.pool.getconn()
            return conn
        except Exception as e:
            raise

    def release_connection(self, conn):
        """
        Libera uma conexão, devolvendo-a ao pool.
        """
        if self.pool is None:
            raise Exception("Pool não iniciado.")
        try:
            self.pool.putconn(conn)
        except Exception as e:
            raise

    def close_pool(self):
        """
        Fecha o pool de conexões.
        """
        if self.pool:
            try:
                self.pool.close()
            except Exception as e:
                raise
        else:
            pass
    
    def get_engine(self):

        return create_engine(
        "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{dbname}".format(
            user=db_user,
            passwd=db_pass,
            host=db_host,
            port=db_port,
            dbname=db_name

        )
        )

postgres_data_manager = PostgreDatabaseManager()
postgres_data_manager.start_pool()