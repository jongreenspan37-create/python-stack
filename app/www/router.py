# Maps API names like "basic/add_numbers" to the Python function that handles them.
# FastAPI comparison: this is your @app.post("/...") decorators, written as one dict.
# To add an endpoint: write the function in scripts/, import it here, add it to ROUTES.
from scripts.basic import add_numbers, add_phrase, add_strings, string_func
from scripts.date_manipulation import adjust_date
from scripts.list_manipulation import count_fruit, upload_fruits, prepare_data
from scripts.health import health
from scripts.create_tables import create_tables, create_f1_tables
from scripts.test import test_1, test_2
from scripts.role_crud import add_role, list_roles, update_role, delete_role
from scripts.user_crud import add_user, list_users, update_user, delete_user
from scripts.crud_drivers import select_drivers_1, select_drivers_2
from scripts.crud_f1 import get_select_options, get_query_by_index


# Explicit route table: a request can only ever reach a function listed
# here. Unlike a getattr()/globals() lookup, a dict can't accidentally
# expose something else in this file's namespace (e.g. a future
# `import os`) -- only names explicitly added to ROUTES are reachable.
ROUTES = {
    "basic/add_numbers": add_numbers,
    "basic/add_phrase": add_phrase,
    "basic/add_strings": add_strings,
    "basic/string_func": string_func,
    "date_manipulation/adjust_date": adjust_date,
    "list_manipulation/count_fruit": count_fruit,
    "list_manipulation/upload_fruits": upload_fruits,
    "list_manipulation/prepare_data": prepare_data,
    "health/health": health,
    "create_tables/create_tables": create_tables,
    "test/test_1": test_1,
    "test/test_2": test_2,
    "role_crud/add_role": add_role,
    "role_crud/list_roles": list_roles,
    "role_crud/update_role": update_role,
    "role_crud/delete_role": delete_role,
    "user_crud/add_user": add_user,
    "user_crud/list_users": list_users,
    "user_crud/update_user": update_user,
    "user_crud/delete_user": delete_user,
    "crud_drivers/select_drivers_1": select_drivers_1, 
    "crud_drivers/select_drivers_2": select_drivers_2, 
    "create_tables/create_f1_tables": create_f1_tables, 
    "crud_f1/get_select_options": get_select_options, 
    "crud_f1/get_query_by_index": get_query_by_index, 

}


# Called by app.py for every /api/run/ request.
# Raises ValueError for unknown names, which app.py turns into a 500 error.
def run_script(name, body):
    func = ROUTES.get(name)
    if func is None:
        raise ValueError(f"unknown endpoint: {name}")
    return func(body)
