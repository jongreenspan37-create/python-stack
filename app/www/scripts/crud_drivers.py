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
            "id": row["id"],
            "driverId": row["driver_id"],
            "url": row["url"],
            "firstName": row["given_name"],
            "lastName": row["family_name"],
            "dateOfBirth": str(row["date_of_birth"]),
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
    sql = """SELECT * FROM drivers ORDER BY id LIMIT 10"""
    return select_drivers(sql)


def select_drivers_2(body=None):
    sql = """SELECT * FROM drivers ORDER BY id LIMIT 10 OFFSET 10"""
    return select_drivers(sql)
     
    