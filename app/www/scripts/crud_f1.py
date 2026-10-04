# Lets formula1.html pick one of the practice queries in f1_queries.py and run it.
from scripts.f1_queries import queries

import sys
from pathlib import Path
from psycopg2.extras import RealDictCursor


sys.path.append(str(Path(__file__).resolve().parent.parent))
from connection import get_connection

# Returns the list of queries for the dropdown (no SQL sent to the browser).
def get_select_options(body=None):
    options = []
    # enumerate gives the position (0, 1, 2...) alongside each item.
    for i, query in enumerate(queries):
        options.append({
            "index": i,
            "title": query["title"],
            "description": query["description"],
            
        })
    return options

# Runs the query the user picked. Body: {"index": 3}
# Only an index is accepted, never SQL, so the page can't run arbitrary SQL.
def get_query_by_index(body=None):
    index = (body or {}).get("index")
    if not isinstance(index, int) or index < 0 or index >= len(queries):
        return {"error": "Invalid index"}
    sql = queries[index]["sql"]
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            return cur.fetchall()
    finally:
            conn.close()
    
if __name__ == "__main__":
    result = get_query_by_index({"index":2})
    print(result)


