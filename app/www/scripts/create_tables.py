
# Creates the database tables: roles/users for the CRUD exercise, and the F1 tables.
import sys
from pathlib import Path
import csv
from scripts.f1_schema import f1_tables

# Add www/ to the import path so `from connection import ...` works even when
# this file is run directly (python3 scripts/create_tables.py).
sys.path.append(str(Path(__file__).resolve().parent.parent))
from connection import get_connection


# Creates the roles and users tables. Plain CREATE TABLE errors if they already
# exist (the error is returned as JSON).
def create_tables(body=None):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Strings side by side inside ( ) are joined automatically into one string.
        sql_roles = ("CREATE TABLE roles ("
                     "id int PRIMARY KEY,"
                     "name varchar(25)"
                     ");")
        # SERIAL = auto-incrementing id. role_id must match a roles.id (foreign key).
        sql_users = ("CREATE TABLE users ( "
                "id SERIAL PRIMARY KEY,"
                "LastName varchar(25),"
                "FirstName varchar(25),"
                "email varchar(50),"
                "role_id int CONSTRAINT fk_role REFERENCES roles(id)"
                ");")

        
        cur.execute(sql_roles)
        cur.execute(sql_users)
        

        

        conn.commit()
        return {"status": "ok", "message": "User and Role tables have been created"}

    except Exception as e:
        return {"status": "error", "detail": str(e)}

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

# Creates each F1 table from f1_schema.py and loads its rows from csv/formula_1/.
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
            # A set of the integer column names, so values can be converted below.
            int_columns = {c for c, t in columns.items() if t in ("INTEGER", "SMALLINT")}
            # One %s per column, e.g. "%s, %s, %s".
            placeholders = ", ".join(["%s"] * len(column_names))
            insert_sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"

            csv_path = BASE_DIR/"csv"/"formula_1"/f"{table_name}.csv"

            with open(csv_path, mode= "r", encoding="utf-8") as file:
                #csv file path
                rows = csv.DictReader(file)

                for row in rows:
                    values = []
                    for column_name in column_names:
                        # Empty CSV cells ("") are stored as NULL.
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








if __name__ == "__main__":
    print(create_tables())

