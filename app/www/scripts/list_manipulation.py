from scripts.get_csv import _read_fruits



def upload_fruits(body=None):
    try:
        fruits = _read_fruits()
    except FileNotFoundError:
        raise FileNotFoundError("fruits.csv not found")
    if not fruits:
        raise ValueError("no fruits found")
    return fruits


def count_fruit(body):
    target = body
    fruits = upload_fruits()
    count = sum(1 for row in fruits if row["fruit"] == target)
    if count == 0:
        return {"error": f'{target} not found'}

    return {"fruit": target, "count": count}

def prepare_data(body=None):
    prepared =[]
    fruits= upload_fruits(None)
    print(fruits)

    for fruit in fruits:
        prepared.append({
            "id" : fruit['id'],
            "description": fruit["fruit"] + " is a sort of fruit"
        })
    return prepared
