from connection import get_connection


def health(body=None):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version(), NOW();")
        version, server_time = cur.fetchone()
        return {"status": "ok", "db_version": version, "server_time": server_time.isoformat()}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    print(health())
