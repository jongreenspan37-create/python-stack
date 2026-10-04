# Earlier standalone version of create_f1_tables(). Not used by router.py.
import sys
from pathlib import Path
import csv


sys.path.append(str(Path(__file__).resolve().parent.parent))
from scripts.f1_schema import f1_tables
from connection import get_connection

def create_f1_tables(body=None):
    try:
        conn = None
        cur = None
        conn = get_connection()
        cur =conn.cursor()

        #base directory with file name stripped outside loop
        BASE_DIR = Path(__file__).resolve().parent

        for table_name, columns in f1_tables.items():
            column_defs =[]
            for column_name, column_type in columns.items():
                #adds the two parts together
                column_defs.append(f"{column_name} {column_type}")

            columns_sql = ",".join(column_defs)
            create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})" 
            cur.execute(create_sql)

            conn.commit()

            column_names = list(columns.keys())
            int_columns = {c for c, t in columns.items() if t in ("INTEGER", "SMALLINT")}
            placeholders = ", ".join(["%s"] * len(column_names))
            insert_sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"

            csv_path = BASE_DIR/"csv"/"formula_1"/f"{table_name}.csv"

            with open(csv_path, mode= "r", encoding="utf-8") as file:
                #csv file path
                rows = csv.DictReader(file)

                for row in rows:
                    values = []
                    for column_name in column_names:
                        value = row[column_name] or None
                        #CSV stores some integer counts as floats (e.g. "1.0")
                        if value is not None and column_name in int_columns:
                            value = int(float(value))
                        values.append(value)
                    cur.execute(insert_sql, tuple(values))

            conn.commit()
                    
        return {"status":"success"}

    except Exception as e:
        return {"failed": "detail: " + str(e)}

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()




