from connection import get_connection


# Database health check: asks PostgreSQL for its version and time.
# If that works, the connection is good.
def health(body=None):
    # Start as None so `finally` knows whether there's anything to close.
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version(), NOW();")
        # fetchone() returns one row as a tuple; unpack it into two variables.
        version, server_time = cur.fetchone()
        return {"status": "ok", "db_version": version, "server_time": server_time.isoformat()}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    # finally always runs (success or error), so the connection is always closed.
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


# Only runs when you execute this file directly: python3 scripts/health.py
if __name__ == "__main__":
    print(health())
