import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection(dbname=None):
    conn_params = {
        "host": os.environ["DB_HOST"],
        "port": os.environ.get("DB_PORT", 5432),
        "dbname": dbname or os.environ["POSTGRES_DB"],
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
    }
    return psycopg2.connect(**conn_params)


conn = get_connection()
cur = conn.cursor()
cur2 = conn.cursor(cursor_factory=RealDictCursor)

sql_create = ("CREATE TABLE IF NOT EXISTS orders (orderID SERIAL PRIMARY KEY,"
              "product_name TEXT);")
sql_drop = "DROP TABLE IF EXISTS orders;"
sql_insert= "INSERT INTO orders (product_name) VALUES (%s);"
values = ("new product",)

sql_pit ="SELECT * FROM drivers;"
#cur.execute(sql_create)
#conn.commit()
cur.execute(sql_pit)
result = cur.fetchone()




new_list = []
new_dict = {}

columns = [d[0] for d in cur.description]
for row in result:
    new_list.append(row)

new_dict = dict(zip(columns, new_list))

print(f"\n Result : {result}")
print(f"\n Cur description built in : {cur.description}")
print(f"\n Example of a list : {new_list}")
print(f"\n Extracted column names : {columns}")
print (f"\n Compiled dict from raw data : {new_dict}")
#conn.commit()

cur2.execute(sql_pit)
easy_dict = cur2.fetchone()
print(easy_dict)
print(easy_dict['url'])
print(columns[2])

