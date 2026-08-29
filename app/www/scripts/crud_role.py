from connection import get_connection

MAX_FIELD_LENGTH = 25


# Two spots to open/close a connection instead of retyping it in every
# function below.
def open_cursor():
    conn = get_connection()
    cur = conn.cursor()
    return conn, cur


def close_cursor(conn, cur):
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()


def add_role(body):
    if not body:
        return {"status": "error", "detail": "missing request body"}

    id = body.get("id")
    name = body.get("name")

    if not id or not name:
        return {"status": "error", "detail": "id and name are required"}

    if len(str(name)) > MAX_FIELD_LENGTH:
        return {"status": "error", "detail": f"name must be {MAX_FIELD_LENGTH} characters or fewer"}

    conn = None
    cur = None
    try:
        conn, cur = open_cursor()
        cur.execute(
            "INSERT INTO roles (id, name) VALUES (%s, %s);",
            (id, name),
        )
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        close_cursor(conn, cur)


def list_roles(body=None):
    conn = None
    cur = None
    try:
        conn, cur = open_cursor()
        cur.execute("SELECT id, name FROM roles ORDER BY id;")
        rows = cur.fetchall()
        roles = [{"id": r[0], "name": r[1]} for r in rows]
        return {"status": "ok", "roles": roles}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        close_cursor(conn, cur)


def get_role(body):
    if not body:
        return {"status": "error", "detail": "missing request body"}

    id = body.get("id")
    if not id:
        return {"status": "error", "detail": "id is required"}

    conn = None
    cur = None
    try:
        conn, cur = open_cursor()
        cur.execute("SELECT id, name FROM roles WHERE id = %s;", (id,))
        row = cur.fetchone()

        if row is None:
            return {"status": "error", "detail": "role not found"}

        return {"status": "ok", "role": {"id": row[0], "name": row[1]}}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        close_cursor(conn, cur)


def update_role(body):
    if not body:
        return {"status": "error", "detail": "missing request body"}

    id = body.get("id")
    name = body.get("name")

    if not id or not name:
        return {"status": "error", "detail": "id and name are required"}

    if len(str(name)) > MAX_FIELD_LENGTH:
        return {"status": "error", "detail": f"name must be {MAX_FIELD_LENGTH} characters or fewer"}

    conn = None
    cur = None
    try:
        conn, cur = open_cursor()
        cur.execute(
            "UPDATE roles SET name = %s WHERE id = %s;",
            (name, id),
        )
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        close_cursor(conn, cur)


def delete_role(body):
    if not body:
        return {"status": "error", "detail": "missing request body"}

    id = body.get("id")

    if not id:
        return {"status": "error", "detail": "id is required"}

    conn = None
    cur = None
    try:
        conn, cur = open_cursor()
        cur.execute("DELETE FROM roles WHERE id = %s;", (id,))
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        close_cursor(conn, cur)
