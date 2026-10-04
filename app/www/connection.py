# Opens a new PostgreSQL connection using psycopg2.
# The settings come from environment variables (set from .env by docker-compose),
# so no password is written in the code.
import os
import psycopg2


def get_connection(dbname=None):
    # os.environ["X"] raises KeyError if X is missing; .get("X", default) doesn't.
    conn_params = {
        "host": os.environ["DB_HOST"],
        "port": os.environ.get("DB_PORT", 5432),
        "dbname": dbname or os.environ["POSTGRES_DB"],
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
    }
    # **conn_params unpacks the dict into keyword arguments: connect(host=..., port=..., ...)
    # The caller must close the connection when finished.
    return psycopg2.connect(**conn_params)
