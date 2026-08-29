from connection import get_connection

MAX_FIELD_LENGTHS = {
    "firstName": 25,
    "lastName": 25,
    "email": 50,
}


# Plain helper functions - not a class, just two spots to open/close a
# connection instead of retyping it in every function below.
def open_cursor():
    conn = get_connection()
    cur = conn.cursor()
    return conn, cur


def close_cursor(conn, cur):
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()




# The class is a blueprint for one row in the "users" table.
# Each User() instance you create holds the data for a single user.
class User:
    # __init__ runs automatically when you write User(...).
    # "self" is the instance being built - every value you attach to
    # self.something becomes a property of that particular user.
    def __init__(self, first_name, last_name, email, id=None, role_id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role_id = role_id

    # A method is just a function that lives on the class and takes
    # "self" as its first argument, so it can read/change that instance's
    # own data. Here, save() inserts (or updates) *this* user in the db.
    def save(self):
        conn = None
        cur = None
        try:
            conn, cur = open_cursor()

            if self.id is None:
                # No id yet -> this user doesn't exist in the db, insert it.
                cur.execute(
                    "INSERT INTO users (FirstName, LastName, email, role_id) "
                    "VALUES (%s, %s, %s, %s) RETURNING id;",
                    (self.first_name, self.last_name, self.email, self.role_id),
                )
                self.id = cur.fetchone()[0]
            else:
                # Already has an id -> update the existing row.
                cur.execute(
                    "UPDATE users SET FirstName = %s, LastName = %s, email = %s, role_id = %s "
                    "WHERE id = %s;",
                    (self.first_name, self.last_name, self.email, self.role_id, self.id),
                )

            conn.commit()
            return {"status": "ok", "id": self.id}
        except Exception as e:
            return {"status": "error", "detail": str(e)}
        finally:
            close_cursor(conn, cur)

    # Another method: turn this instance back into the dict shape the
    # frontend expects (camelCase keys instead of the snake_case attrs).
    def to_dict(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "roleId": self.role_id,
        }


def _check_field_lengths(**fields):
    for label, value in fields.items():
        max_length = MAX_FIELD_LENGTHS[label]
        if value and len(value) > max_length:
            return f"{label} must be {max_length} characters or fewer"
    return None


# This is the "example of using the class": build a User instance from
# the request body, then call its .save() method to hit the database.
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

    # Instantiate the class -> this is just a Python object in memory,
    # nothing has touched the database yet.
    user = User(first_name=first_name, last_name=last_name, email=email, role_id=role_id)

    # Now call the method on that instance to actually write it to the db.
    return user.save()


# UserView is a different class from User because it models a different
# thing: not one row of "users", but one row of "users LEFT JOIN roles"
# - the same idea as an Access saved query or a SQL "CREATE VIEW". It's
# only ever built from that joined query, and it's read-only: no save()
# or delete(), because there's no single table to write a "joined row"
# back to - you'd update users and roles separately if you needed that.
class UserView:

    def __init__(self, id, first_name, last_name, email, role_id, role_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role_id = role_id
        self.role_name = role_name

    def to_dict(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "roleId": self.role_id,
            "roleName": self.role_name,
        }


# Using UserView: run the joined query, then build one UserView per row.
def list_users(body=None):
    conn = None
    cur = None
    try:
        conn, cur = open_cursor()
        cur.execute(
            "SELECT u.id, u.FirstName, u.LastName, u.email, u.role_id, r.name "
            "FROM users u LEFT JOIN roles r ON u.role_id = r.id "
            "ORDER BY u.id;"
        )
        rows = cur.fetchall()

        # row is a tuple of 6 values, in the same order as the SELECT list,
        # so *row unpacks it straight into UserView's constructor args.
        users = [UserView(*row).to_dict() for row in rows]

        return {"status": "ok", "users": users}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        close_cursor(conn, cur)


# Same join as list_users, but with a WHERE on id so it returns just one
# UserView instead of building one per row.
def get_user(body):
    if not body:
        return {"status": "error", "detail": "missing request body"}

    user_id = body.get("id")
    if not user_id:
        return {"status": "error", "detail": "id is required"}

    conn = None
    cur = None
    try:
        conn, cur = open_cursor()
        cur.execute(
            "SELECT u.id, u.FirstName, u.LastName, u.email, u.role_id, r.name "
            "FROM users u LEFT JOIN roles r ON u.role_id = r.id "
            "WHERE u.id = %s;",
            (user_id,),
        )
        row = cur.fetchone()

        if row is None:
            return {"status": "error", "detail": "user not found"}

        return {"status": "ok", "user": UserView(*row).to_dict()}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        close_cursor(conn, cur)


# Deleting only needs an id, not a full first_name/last_name/email set,
# so this stays a plain function rather than going through User.
def delete_user(body):
    if not body:
        return {"status": "error", "detail": "missing request body"}

    user_id = body.get("id")
    if not user_id:
        return {"status": "error", "detail": "id is required"}

    conn = None
    cur = None
    try:
        conn, cur = open_cursor()
        cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        close_cursor(conn, cur)


if __name__ == "__main__":
    result = add_user({"firstName": "Test", "lastName": "User", "email": "test@example.com"})
    print(result)

