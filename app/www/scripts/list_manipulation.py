from scripts.get_csv import _read_fruits



def upload_fruits(body=None):
    try:
        fruits = _read_fruits()
    except FileNotFoundError:
        return {"error": "fruits.csv not found"}
    if not fruits:
        return {"error": "no fruits found"}
    return fruits


def count_fruit(body):

    try:
        target = body
        fruits = _read_fruits()
        count = sum(1 for row in fruits if row["fruit"] == target)
    except FileNotFoundError:
        return {"error": "fruits.csv not found"}
    if count == 0:
        return {"error": f'{target} not found'}

    return {"fruit": target, "count": count}

def prepare_data(fruits):
    prepared =[]
    for fruit in fruits:
        prepared.append({
            "description":fruit["fruit"] + " is a fruit"
        })
    return prepared
