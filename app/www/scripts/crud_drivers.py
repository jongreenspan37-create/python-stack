# Reads F1 drivers from the database. Used by f1tables.html.
import sys
from pathlib import Path
from psycopg2.extras import RealDictCursor


sys.path.append(str(Path(__file__).resolve().parent.parent))
from connection import get_connection

# Runs a drivers query and renames the columns to camelCase for the page.
def select_drivers(sql):
    try:
        conn = None
        cur =None
        conn = get_connection()
        # RealDictCursor returns each row as a dict ({"driverid": ..}) instead of a tuple.
        cur = conn.cursor(cursor_factory=RealDictCursor)

        
        cur.execute(sql)
        rows = cur.fetchall()

        #not requred but creates javascript style names and DOB works either way 
        #but this ensures gets set as a string
        result = [
        {
            
            "driverId": row["driverid"],
            "url": row["url"],
            "firstName": row["givenname"],
            "lastName": row["familyname"],
            "dateOfBirth": str(row["dateofbirth"]),
            "nationality": row["nationality"],
        }
        for row in rows
    ]

        return result
    
    except Exception as e:
            return {"error": "details " + str(e)}
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# First 10 drivers, all columns as stored.
def select_drivers_1(body=None):
    sql = "SELECT * FROM drivers ORDER BY id LIMIT 10"
    conn = get_connection()
    try:
        # `with` closes the cursor automatically when the block ends.
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            return cur.fetchall()
    finally:
        conn.close()


# Drivers 11-20 (OFFSET 10 skips the first 10), with camelCase names.
def select_drivers_2(body=None):
    sql = """SELECT * FROM drivers ORDER BY driverid LIMIT 10 OFFSET 10"""
    return select_drivers(sql)
     
    