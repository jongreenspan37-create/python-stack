import sys
from pathlib import Path
import csv

sys.path.append(str(Path(__file__).resolve().parent.parent))
from connection import get_connection



def create_driver_table():
    try:
        conn = None
        cur = None
        conn = get_connection()
        cur =conn.cursor()
        sql = ("""
            CREATE TABLE IF NOT EXISTS drivers (
                id SERIAL PRIMARY KEY,
                driver_id TEXT NOT NULL,
                url TEXT NOT NULL,
                given_name TEXT NOT NULL,
                family_name TEXT NOT NULL,
                date_of_birth DATE,
                nationality TEXT
            )
        """)
        cur.execute("DROP TABLE IF EXISTS drivers")
        cur.execute(sql)
        conn.commit()
        #base directory with file name stripped
        BASE_DIR = Path(__file__).resolve().parent
        #csv file path
        csv_path = BASE_DIR/"csv"/"formula_1"/"drivers.csv"
        insert_sql = """INSERT INTO drivers (driver_id, url, given_name, family_name, date_of_birth, nationality) VALUES (%s, %s, %s, %s, %s, %s)"""
        with open(csv_path, mode= "r", encoding="utf-8") as file:
           rows = csv.DictReader(file)

           for row in rows:
                cur.execute(insert_sql,
                          (
                            row["driverId"],
                            row["url"],
                            row["GivenName"],
                            row["FamilyName"],
                            row["DateOfBirth"],
                            row["Nationality"],
                          ))
                  
                

        conn.commit()       
        return {"status":"success"}



    except Exception as e:
        return {"status":"error", "detail": str(e)}
    finally:
        if cur:
           cur.close()
        if conn:
         conn.close()

if __name__ == "__main__":
    result = create_driver_table()
    print(result)


