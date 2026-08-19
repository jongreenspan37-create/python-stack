from connection import get_connection


def add_user(body):
    if not body:
        return {"status": "error", "detail": "missing request body"}

    first_name = body.get("firstName")
    last_name = body.get("lastName")
    email = body.get("email")

    if not first_name or not last_name or not email:
        return {"status": "error", "detail": "firstName, lastName and email are required"}

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (FirstName, LastName, email) VALUES (%s, %s, %s) RETURNING id;",
            (first_name, last_name, email),
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


if __name__ == "__main__":
    print(add_user({"firstName": "Test", "lastName": "User", "email": "test@example.com"}))
