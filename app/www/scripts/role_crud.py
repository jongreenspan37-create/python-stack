# CRUD (Create, Read, Update, Delete) for the roles table.
# Called from the roles form/table in script.js on database-interaction.html.
# Every function follows the same pattern: validate the body, open a connection,
# run the SQL, then close the connection in `finally`.
from connection import get_connection

# Matches the varchar(25) column size, so too-long names get a clear error
# instead of a database error.
MAX_FIELD_LENGTH = 25


# Inserts a new role. Body: {"id": .., "name": ..}
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
        conn = get_connection()
        # A cursor runs SQL and holds the results.
        cur = conn.cursor()
        # %s placeholders: psycopg2 sends the values separately from the SQL,
        # which prevents SQL injection. Never build SQL with f-strings from user input.
        cur.execute(
            "INSERT INTO roles (id, name) VALUES (%s, %s);",
            (id, name),
        )
        # psycopg2 doesn't save changes until you commit.
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    # finally always runs, so the connection is closed even after an error.
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


# Returns {"status": "ok", "roles": [{"id": 1, "name": "Admin"}, ...]}
def list_roles(body=None):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM roles ORDER BY id;")
        rows = cur.fetchall()
        # Rows come back as tuples (1, "Admin"); turn each into a dict for the JSON.
        roles = [{"id": r[0], "name": r[1]} for r in rows]
        return {"status": "ok", "roles": roles}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


# Renames a role. Body: {"id": .., "name": ..}
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


# Deletes a role. Body: {"id": ..}
# Fails if a user still has this role, because of the foreign key on users.role_id.
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
        # (id,) with a comma is a one-item tuple; (id) would just be id.
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
