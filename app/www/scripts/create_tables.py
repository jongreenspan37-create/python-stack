from connection import get_connection


def create_tables(body=None):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        sql_roles = ("CREATE TABLE roles ("
                     "id int PRIMARY KEY,"
                     "name varchar(255)"
                     ");")
        sql_users = ("CREATE TABLE users ( "
                "id SERIAL PRIMARY KEY,"
                "LastName varchar(255),"
                "FirstName varchar(255),"
                "email varchar(255),"
                "role_id int CONSTRAINT fk_role REFERENCES roles(id)"
                ");")
        cur.execute(sql_roles)
        cur.execute(sql_users)
        conn.commit()
        return {"status": "ok", "message": "User and Role tables have been created"}

    except Exception as e:
        return {"status": "error", "detail": str(e)}

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()



if __name__ == "__main__":
    print(create_tables())

