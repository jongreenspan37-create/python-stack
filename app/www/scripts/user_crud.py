from connection import get_connection

MAX_FIELD_LENGTHS = {
    "firstName": 25,
    "lastName": 25,
    "email": 50,
}


def _check_field_lengths(**fields):
    for label, value in fields.items():
        max_length = MAX_FIELD_LENGTHS[label]
        if value and len(value) > max_length:
            return f"{label} must be {max_length} characters or fewer"
    return None


def add_user(body):
    if not body:
        return {"status": "error", "detail": "missing request body"}

    first_name = body.get("firstName")
    last_name = body.get("lastName")
    email = body.get("email")
    role_id = body.get("roleId") or None

    if not first_name or not last_name or not email:
        return {"status": "error", "detail": "firstName, lastName and email are required"}

    length_error = _check_field_lengths(firstName=first_name, lastName=last_name, email=email)
    if length_error:
        return {"status": "error", "detail": length_error}

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (FirstName, LastName, email, role_id) VALUES (%s, %s, %s, %s) RETURNING id;",
            (first_name, last_name, email, role_id),
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        return {"status": "ok", "id": new_id}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def list_users(body=None):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT u.id, u.FirstName, u.LastName, u.email, u.role_id, r.name "
            "FROM users u LEFT JOIN roles r ON u.role_id = r.id "
            "ORDER BY u.id;"
        )
        rows = cur.fetchall()
        users = [
            {
                "id": r[0],
                "firstName": r[1],
                "lastName": r[2],
                "email": r[3],
                "roleId": r[4],
                "roleName": r[5],
            }
            for r in rows
        ]
        return {"status": "ok", "users": users}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def update_user(body):
    if not body:
        return {"status": "error", "detail": "missing request body"}

    user_id = body.get("id")
    first_name = body.get("firstName")
    last_name = body.get("lastName")
    email = body.get("email")
    role_id = body.get("roleId") or None

    if not user_id or not first_name or not last_name or not email:
        return {"status": "error", "detail": "id, firstName, lastName and email are required"}

    length_error = _check_field_lengths(firstName=first_name, lastName=last_name, email=email)
    if length_error:
        return {"status": "error", "detail": length_error}

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET FirstName = %s, LastName = %s, email = %s, role_id = %s WHERE id = %s;",
            (first_name, last_name, email, role_id, user_id),
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


def delete_user(body):
    if not body:
        return {"status": "error", "detail": "missing request body"}

    user_id = body.get("id")

    if not user_id:
        return {"status": "error", "detail": "id is required"}

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    print(add_user({"firstName": "Test", "lastName": "User", "email": "test@example.com"}))
