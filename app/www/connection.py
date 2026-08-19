import os
import psycopg2


def get_connection(dbname=None):
    conn_params = {
        "host": os.environ["DB_HOST"],
        "port": os.environ.get("DB_PORT", 5432),
        "dbname": dbname or os.environ["POSTGRES_DB"],
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
    }
    return psycopg2.connect(**conn_params)
