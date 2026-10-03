import sys
from pathlib import Path
from psycopg2.extras import RealDictCursor


sys.path.append(str(Path(__file__).resolve().parent.parent))
from connection import get_connection

def select_drivers(sql):
    try:
        conn = None
        cur =None
        conn = get_connection()
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

def select_drivers_1(body=None):
    sql = "SELECT * FROM drivers ORDER BY id LIMIT 10"
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            return cur.fetchall()
    finally:
        conn.close()


def select_drivers_2(body=None):
    sql = """SELECT * FROM drivers ORDER BY driverid LIMIT 10 OFFSET 10"""
    return select_drivers(sql)
     
    