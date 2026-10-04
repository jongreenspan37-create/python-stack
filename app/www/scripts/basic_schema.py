# Practice: describing tables as data (a dict of columns). Not used by router.py.

database_tables = {
    "roles": {
        "columns": [
            {"name": "id", "data_type": "SERIAL", "constraint": "PRIMARY KEY"},
            {"name": "rank", "data_type": "INT", "constraint": "NOT NULL"},
            {"name": "name", "data_type": "TEXT", "constraint": "NOT NULL"},
        ],
    },
    "users": {
        "columns": [
            {"name": "id", "data_type": "SERIAL", "constraint": "PRIMARY KEY"},
                        {"name": "first_name", "data_type": "TEXT", "constraint": "NOT NULL"},
                        {"name": "last_name", "data_type": "TEXT", "constraint": "NOT NULL"},
                        {"name": "email", "data_type": "TEXT", "constraint": "NOT NULL"},
                        {"name": "hashed_password", "data_type": "TEXT", "constraint": "NOT NULL"},
                        {"name": "created_at", "data_type": "TIMESTAMPTZ", "constraint": "NOT NULL"},
                        {"name": "role_id", "data_type": "INTEGER", "constraint": "NOT NULL"},
        ],
        "indexes": [
            {"name": "users_email_lower_idx", "on": "LOWER(email)", "unique": True},
        ],
        "foreign_keys": [
            {
                "name": "fk_users_role",
                "column": "role_id",
                "references_table": "roles",
                "references_column": "id",
                "on_delete": "RESTRICT",  # this is actually the default
            },
        ],
    },
} 

#1. top level values
for data in database_tables.values():
    print(f"\n This is the first loop {data}")

#2. next level
for table, table_def in database_tables.items():
    for test in table_def:
        print(f"\n This is the second loop {test}")

#3. next level plus dict
for table, table_def in database_tables.items():
    print(f"\nItem Three {table_def}")

#4. 
all_table_defs = [table_def for table, table_def in database_tables.items()]
print(f"\nThis IS {table} {all_table_defs}")

#5. just column names in a list
for key, table_def in database_tables.items():
    insert_cols = []
    insert_place = []
    for col in table_def["columns"]:
        insert_cols.append(col['name'])
        insert_place.append('%s')
    cols_string = ", ".join(insert_cols)
    place_string = ", ".join(insert_place)
    print(f"INSERT INTO {key} ({cols_string}) VALUES ({place_string})")
        
    new_col = [col for col in table_def['columns']]
    print(f"\n Shortcut {new_col}")

#format

txt = "My name is {0}, I am {1}".format('n','the')
print(txt)

x = 5 | 3
print(f"x= {x}")

a = (bin(5))
b= (bin(3))
c= 5 << 2
print(c)

set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

set3 = set1.union(set2)
print(set3)

set4 = {"a", "b", "c"}
set5 = {1, 2, 3}

set6 = set4 | set5
print(set6)