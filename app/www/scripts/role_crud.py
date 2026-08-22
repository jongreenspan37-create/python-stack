from connection import get_connection


def add_role(body):
    if not body:
        return {"status": "error", "detail": "missing request body"}

    id = body.get("id")
    name = body.get("name")

    if not id or not name:
        return {"status": "error", "detail": "id and name are required"}

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO roles (id, name) VALUES (%s, %s);",
            (id, name),
        )
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def list_roles(body=None):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM roles ORDER BY id;")
        rows = cur.fetchall()
        roles = [{"id": r[0], "name": r[1]} for r in rows]
        return {"status": "ok", "roles": roles}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def update_role(body):
    if not body:
        return {"status": "error", "detail": "missing request body"}

    id = body.get("id")
    name = body.get("name")

    if not id or not name:
        return {"status": "error", "detail": "id and name are required"}

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE roles SET name = %s WHERE id = %s;",
            (name, id),
        )
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def delete_role(body):
    if not body:
        return {"status": "error", "detail": "missing request body"}

    id = body.get("id")

    if not id:
        return {"status": "error", "detail": "id is required"}

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM roles WHERE id = %s;", (id,))
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
