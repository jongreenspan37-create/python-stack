from connection import get_connection


def create_tables(body=None):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        sql_roles = ("CREATE TABLE roles ("
                     "id int PRIMARY KEY,"
                     "name varchar(25)"
                     ");")
        sql_users = ("CREATE TABLE users ( "
                "id SERIAL PRIMARY KEY,"
                "LastName varchar(25),"
                "FirstName varchar(25),"
                "email varchar(50),"
                "role_id int CONSTRAINT fk_role REFERENCES roles(id)"
                ");")
        cur.execute(sql_roles)
        cur.execute(sql_users)

        cur.execute("""
            CREATE OR REPLACE FUNCTION check_roles_row_limit() RETURNS TRIGGER AS $$
            BEGIN
                IF (SELECT COUNT(*) FROM roles) >= 3 THEN
                    RAISE EXCEPTION 'roles table row limit (3) reached';
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        cur.execute("""
            CREATE TRIGGER roles_row_limit
            BEFORE INSERT ON roles
            FOR EACH ROW EXECUTE FUNCTION check_roles_row_limit();
        """)

        cur.execute("""
            CREATE OR REPLACE FUNCTION check_users_row_limit() RETURNS TRIGGER AS $$
            BEGIN
                IF (SELECT COUNT(*) FROM users) >= 5 THEN
                    RAISE EXCEPTION 'users table row limit (5) reached';
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        cur.execute("""
            CREATE TRIGGER users_row_limit
            BEFORE INSERT ON users
            FOR EACH ROW EXECUTE FUNCTION check_users_row_limit();
        """)

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

